/////////////////////////////////////////////////////////////////////////////
// Name:        harm.h
// Author:      Laurent Pugin
// Created:     2016
// Copyright (c) Authors and others. All rights reserved.
/////////////////////////////////////////////////////////////////////////////

#ifndef __VRV_HARM_H__
#define __VRV_HARM_H__

#include "controlelement.h"
#include "textdirinterface.h"
#include "timeinterface.h"
#include "transposition.h"

namespace vrv {

class TextElement;

//----------------------------------------------------------------------------
// Harm (harmony)
//----------------------------------------------------------------------------

/**
 * This class models the MEI <harm> element.
 */
class Harm : public ControlElement,
             public TextListInterface,
             public TextDirInterface,
             public TimeSpanningInterface,
             public AttLang,
             public AttNNumberLike {
public:
    /**
     * @name Constructors, destructors, and other standard methods
     * Reset method reset all attribute classes
     */
    ///@{
    Harm();
    virtual ~Harm();
    Object *Clone() const override { return new Harm(*this); }
    void Reset() override;
    std::string GetClassName() const override { return "Harm"; }
    ///@}

    /**
     * @name Getter to interfaces
     */
    ///@{
    TextDirInterface *GetTextDirInterface() override { return dynamic_cast<TextDirInterface *>(this); }
    TimePointInterface *GetTimePointInterface() override { return dynamic_cast<TimePointInterface *>(this); }
    TimeSpanningInterface *GetTimeSpanningInterface() override { return dynamic_cast<TimeSpanningInterface *>(this); }
    ///@}

    /**
     * Add an element (text, rend. etc.) to a harm.
     * Only supported elements will be actually added to the child list.
     */
    bool IsSupportedChild(Object *object) override;

    /**
     * Transposition related. The int tracks where we have iterated through the string.
     */
    bool GetRootPitch(TransPitch &pitch, unsigned int &pos);
    void SetRootPitch(const TransPitch &pitch, unsigned int endPos);
    bool GetBassPitch(TransPitch &pitch);
    void SetBassPitch(const TransPitch &pitch);

    //----------//
    // Functors //
    //----------//

    /**
     * See Object::PrepareFloatingGrps
     */
    int PrepareFloatingGrps(FunctorParams *functorParams) override;

    /**
     * See Object::AdjustHarmGrpsSpacing
     */
    int AdjustHarmGrpsSpacing(FunctorParams *functorParams) override;

    /**
     * See Object::Transpose
     */
    int Transpose(FunctorParams *functorParams) override;

protected:
    //
private:
    //
public:
    //
private:
    //
};

} // namespace vrv

#endif
