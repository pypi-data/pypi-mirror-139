/////////////////////////////////////////////////////////////////////////////
// Name:        tabgrp.cpp
// Author:      Laurent Pugin
// Created:     2019
// Copyright (c) Authors and others. All rights reserved.
/////////////////////////////////////////////////////////////////////////////

#include "tabgrp.h"

//----------------------------------------------------------------------------

#include <assert.h>

//----------------------------------------------------------------------------

#include "editorial.h"
#include "functorparams.h"
#include "note.h"
#include "tabdursym.h"

namespace vrv {

//----------------------------------------------------------------------------
// TabGrp
//----------------------------------------------------------------------------

static const ClassRegistrar<TabGrp> s_factory("tabGrp", TABGRP);

TabGrp::TabGrp() : LayerElement(TABGRP, "tabgrp-"), ObjectListInterface(), DurationInterface()
{
    this->RegisterInterface(DurationInterface::GetAttClasses(), DurationInterface::IsInterface());

    this->Reset();
}

TabGrp::~TabGrp() {}

void TabGrp::Reset()
{
    LayerElement::Reset();
    DurationInterface::Reset();
}

bool TabGrp::IsSupportedChild(Object *child)
{
    if (child->Is(NOTE)) {
        assert(dynamic_cast<Note *>(child));
    }
    else if (child->Is(TABDURSYM)) {
        assert(dynamic_cast<TabDurSym *>(child));
    }
    else if (child->IsEditorialElement()) {
        assert(dynamic_cast<EditorialElement *>(child));
    }
    else {
        return false;
    }
    return true;
}

void TabGrp::FilterList(ArrayOfObjects *childList)
{
    // Retain only note children of chords
    ArrayOfObjects::iterator iter = childList->begin();

    while (iter != childList->end()) {
        iter = ((*iter)->Is(NOTE)) ? iter + 1 : childList->erase(iter);
    }

    std::sort(childList->begin(), childList->end(), TabCourseSort());
}

int TabGrp::GetYTop()
{
    const ArrayOfObjects *childList = this->GetList(this); // make sure it's initialized
    assert(childList->size() > 0);

    // The last note is the top
    return childList->back()->GetDrawingY();
}

int TabGrp::GetYBottom()
{
    const ArrayOfObjects *childList = this->GetList(this); // make sure it's initialized
    assert(childList->size() > 0);

    // The first note is the bottom
    return childList->front()->GetDrawingY();
}

Note *TabGrp::GetTopNote()
{
    const ArrayOfObjects *childList = this->GetList(this); // make sure it's initialized
    assert(childList->size() > 0);

    Note *topNote = vrv_cast<Note *>(childList->back());
    assert(topNote);
    return topNote;
}

Note *TabGrp::GetBottomNote()
{
    const ArrayOfObjects *childList = this->GetList(this); // make sure it's initialized
    assert(childList->size() > 0);

    // The first note is the bottom
    Note *bottomNote = vrv_cast<Note *>(childList->front());
    assert(bottomNote);
    return bottomNote;
}

//----------------------------------------------------------------------------
// Functor methods
//----------------------------------------------------------------------------

int TabGrp::CalcOnsetOffsetEnd(FunctorParams *functorParams)
{
    CalcOnsetOffsetParams *params = vrv_params_cast<CalcOnsetOffsetParams *>(functorParams);
    assert(params);

    LayerElement *element = this->ThisOrSameasAsLink();

    double incrementScoreTime = element->GetAlignmentDuration(
        params->m_currentMensur, params->m_currentMeterSig, true, params->m_notationType);
    incrementScoreTime = incrementScoreTime / (DUR_MAX / DURATION_4);
    double realTimeIncrementSeconds = incrementScoreTime * 60.0 / params->m_currentTempo;

    params->m_currentScoreTime += incrementScoreTime;
    params->m_currentRealTimeSeconds += realTimeIncrementSeconds;

    return FUNCTOR_CONTINUE;
}

int TabGrp::CalcStem(FunctorParams *functorParams)
{
    CalcStemParams *params = vrv_params_cast<CalcStemParams *>(functorParams);
    assert(params);

    params->m_dur = this->GetActualDur();
    params->m_tabGrpWithNoNote = (!this->FindDescendantByType(NOTE));

    return FUNCTOR_CONTINUE;
}

} // namespace vrv
