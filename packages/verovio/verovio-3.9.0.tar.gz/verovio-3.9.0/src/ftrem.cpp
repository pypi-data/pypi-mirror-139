/////////////////////////////////////////////////////////////////////////////
// Name:        ftrem.cpp
// Author:      Klaus Rettinghaus
// Created:     2017
// Copyright (c) Authors and others. All rights reserved.
/////////////////////////////////////////////////////////////////////////////

#include "ftrem.h"

//----------------------------------------------------------------------------

#include <assert.h>
#include <math.h>

//----------------------------------------------------------------------------

#include "chord.h"
#include "editorial.h"
#include "functorparams.h"
#include "layer.h"
#include "note.h"
#include "staff.h"
#include "vrv.h"

//----------------------------------------------------------------------------

#include "MidiFile.h"

namespace vrv {

//----------------------------------------------------------------------------
// FTrem
//----------------------------------------------------------------------------

static const ClassRegistrar<FTrem> s_factory("fTrem", FTREM);

FTrem::FTrem() : LayerElement(FTREM, "ftrem-"), BeamDrawingInterface(), AttFTremVis(), AttTremMeasured()
{
    this->RegisterAttClass(ATT_FTREMVIS);
    this->RegisterAttClass(ATT_TREMMEASURED);

    this->Reset();
}

FTrem::~FTrem() {}

void FTrem::Reset()
{
    LayerElement::Reset();
    BeamDrawingInterface::Reset();
    this->ResetFTremVis();
    this->ResetTremMeasured();
}

bool FTrem::IsSupportedChild(Object *child)
{
    if (child->Is(CHORD)) {
        assert(dynamic_cast<Chord *>(child));
    }
    else if (child->Is(CLEF)) {
        assert(dynamic_cast<Clef *>(child));
    }
    else if (child->Is(NOTE)) {
        assert(dynamic_cast<Note *>(child));
    }
    else if (child->IsEditorialElement()) {
        assert(dynamic_cast<EditorialElement *>(child));
    }
    else {
        return false;
    }
    return true;
}

const ArrayOfBeamElementCoords *FTrem::GetElementCoords()
{
    this->GetList(this);

    return &m_beamElementCoords;
}

void FTrem::FilterList(ArrayOfObjects *childList)
{
    ArrayOfObjects::iterator iter = childList->begin();

    while (iter != childList->end()) {
        if (!(*iter)->Is(NOTE) && !(*iter)->Is(CHORD)) {
            // remove anything that is not an LayerElement (e.g. Verse, Syl, etc.)
            iter = childList->erase(iter);
            continue;
        }
        // also remove notes within chords
        if ((*iter)->Is(NOTE)) {
            Note *note = vrv_cast<Note *>(*iter);
            assert(note);
            if (note->IsChordTone()) {
                iter = childList->erase(iter);
                continue;
            }
        }
        ++iter;
    }

    Staff *staff = this->GetAncestorStaff();

    this->InitCoords(childList, staff, BEAMPLACE_NONE);
    this->InitCue(false);
}

std::pair<int, int> FTrem::GetAdditionalBeamCount() const
{
    return { std::max(this->GetBeams(), this->GetBeamsFloat()), 0 };
}

std::pair<int, int> FTrem::GetFloatingBeamCount() const
{
    return { this->GetBeams(), this->GetBeamsFloat() };
}

//----------------------------------------------------------------------------
// Functors methods
//----------------------------------------------------------------------------

int FTrem::CalcStem(FunctorParams *functorParams)
{
    CalcStemParams *params = vrv_params_cast<CalcStemParams *>(functorParams);
    assert(params);

    const ArrayOfObjects *fTremChildren = this->GetList(this);

    // Should we assert this at the beginning?
    if (fTremChildren->empty()) {
        return FUNCTOR_CONTINUE;
    }

    if (this->GetElementCoords()->size() != 2) {
        LogError("Stem calculation: <fTrem> element has invalid number of descendants.");
        return FUNCTOR_CONTINUE;
    }

    m_beamSegment.InitCoordRefs(this->GetElementCoords());

    Layer *layer = vrv_cast<Layer *>(this->GetFirstAncestor(LAYER));
    assert(layer);
    Staff *staff = vrv_cast<Staff *>(layer->GetFirstAncestor(STAFF));
    assert(staff);

    m_beamSegment.CalcBeam(layer, staff, params->m_doc, this);

    return FUNCTOR_CONTINUE;
}

int FTrem::ResetDrawing(FunctorParams *functorParams)
{
    // Call parent one too
    LayerElement::ResetDrawing(functorParams);

    m_beamSegment.Reset();

    // We want the list of the ObjectListInterface to be re-generated
    this->Modify();
    return FUNCTOR_CONTINUE;
}

int FTrem::GenerateMIDI(FunctorParams *functorParams)
{
    // GenerateMIDIParams *params = vrv_params_cast<GenerateMIDIParams *>(functorParams);
    // assert(params);

    FTrem *fTrem = vrv_cast<FTrem *>(this);
    assert(fTrem);

    if (!fTrem->HasUnitdur()) {
        return FUNCTOR_CONTINUE;
    }
    else {
        LogWarning("FTrem produces incorrect MIDI output");
    }

    return FUNCTOR_CONTINUE;
}

} // namespace vrv
