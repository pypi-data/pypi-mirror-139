/////////////////////////////////////////////////////////////////////////////
// Name:        textdirinterface.cpp
// Author:      Laurent Pugin
// Created:     2015
// Copyright (c) Authors and others. All rights reserved.
/////////////////////////////////////////////////////////////////////////////

#include "textdirinterface.h"

//----------------------------------------------------------------------------

#include <assert.h>

//----------------------------------------------------------------------------

#include "comparison.h"
#include "vrv.h"

namespace vrv {

//----------------------------------------------------------------------------
// TextDirInterface
//----------------------------------------------------------------------------

TextDirInterface::TextDirInterface() : Interface(), AttPlacementRelStaff()
{
    this->RegisterInterfaceAttClass(ATT_PLACEMENTRELSTAFF);

    this->Reset();
}

TextDirInterface::~TextDirInterface() {}

void TextDirInterface::Reset()
{
    this->ResetPlacementRelStaff();
}

int TextDirInterface::GetNumberOfLines(Object *object)
{
    assert(object);

    ListOfObjects lbs = object->FindAllDescendantsByType(LB);
    return ((int)lbs.size() + 1);
}

} // namespace vrv
