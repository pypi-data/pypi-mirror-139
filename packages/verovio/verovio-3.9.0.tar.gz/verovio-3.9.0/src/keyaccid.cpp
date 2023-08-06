/////////////////////////////////////////////////////////////////////////////
// Name:        keyaccid.cpp
// Author:      Laurent Pugin
// Created:     2019
// Copyright (c) Authors and others. All rights reserved.
/////////////////////////////////////////////////////////////////////////////

#include "keyaccid.h"

//----------------------------------------------------------------------------

#include <assert.h>

//----------------------------------------------------------------------------

#include "accid.h"
#include "doc.h"
#include "editorial.h"
#include "functorparams.h"
#include "keysig.h"
#include "note.h"
#include "smufl.h"
#include "vrv.h"

namespace vrv {

//----------------------------------------------------------------------------
// KeyAccid
//----------------------------------------------------------------------------

static const ClassRegistrar<KeyAccid> s_factory("keyAccid", KEYACCID);

KeyAccid::KeyAccid()
    : LayerElement(KEYACCID, "keyaccid-"), PitchInterface(), AttAccidental(), AttColor(), AttEnclosingChars()
{

    this->RegisterInterface(PitchInterface::GetAttClasses(), PitchInterface::IsInterface());
    this->RegisterAttClass(ATT_ACCIDENTAL);
    this->RegisterAttClass(ATT_COLOR);
    this->RegisterAttClass(ATT_ENCLOSINGCHARS);

    this->Reset();
}

KeyAccid::~KeyAccid() {}

void KeyAccid::Reset()
{
    LayerElement::Reset();
    PitchInterface::Reset();
    this->ResetAccidental();
    this->ResetColor();
    this->ResetEnclosingChars();
}

bool KeySig::IsSupportedChild(Object *child)
{
    if (this->IsAttribute()) {
        LogError("Adding a child to an attribute is not allowed");
        assert(false);
    }
    else if (child->Is(KEYACCID)) {
        assert(dynamic_cast<KeyAccid *>(child));
    }
    else if (child->IsEditorialElement()) {
        assert(dynamic_cast<EditorialElement *>(child));
    }
    else {
        return false;
    }
    return true;
}

std::wstring KeyAccid::GetSymbolStr() const
{
    if (!this->HasAccid()) return L"";

    wchar_t symc = Accid::GetAccidGlyph(this->GetAccid());
    std::wstring symbolStr;

    if (this->HasEnclose()) {
        switch (this->GetEnclose()) {
            case ENCLOSURE_brack:
                symbolStr.push_back(SMUFL_E26C_accidentalBracketLeft);
                symbolStr.push_back(symc);
                symbolStr.push_back(SMUFL_E26D_accidentalBracketRight);
                break;
            case ENCLOSURE_paren:
                symbolStr.push_back(SMUFL_E26A_accidentalParensLeft);
                symbolStr.push_back(symc);
                symbolStr.push_back(SMUFL_E26B_accidentalParensRight);
                break;
            default: symbolStr.push_back(symc);
        }
    }
    else {
        symbolStr.push_back(symc);
    }
    return symbolStr;
}

//----------------------------------------------------------------------------
// Functor methods
//----------------------------------------------------------------------------

} // namespace vrv
