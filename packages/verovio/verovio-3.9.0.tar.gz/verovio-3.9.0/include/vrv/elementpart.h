/////////////////////////////////////////////////////////////////////////////
// Name:        elementpart.h
// Author:      Laurent Pugin
// Created:     2017
// Copyright (c) Authors and others. All rights reserved.
/////////////////////////////////////////////////////////////////////////////

#ifndef __VRV_ELEMENT_PART_H__
#define __VRV_ELEMENT_PART_H__

#include "atts_cmn.h"
#include "atts_shared.h"
#include "atts_visual.h"
#include "layerelement.h"

namespace vrv {

class TupletNum;

//----------------------------------------------------------------------------
// Dots
//----------------------------------------------------------------------------

/**
 * This class models a group of dots as a layer element part and has not direct MEI equivlatent.
 */
class Dots : public LayerElement, public AttAugmentDots {
public:
    /**
     * @name Constructors, destructors, reset and class name methods
     * Reset method resets all attribute classes
     */
    ///@{
    Dots();
    virtual ~Dots();
    void Reset() override;
    std::string GetClassName() const override { return "Dots"; }
    ///@}

    /** Override the method since alignment is required */
    bool HasToBeAligned() const override { return true; }

    std::set<int> GetDotLocsForStaff(Staff *staff) const;
    std::set<int> &ModifyDotLocsForStaff(Staff *staff);

    const MapOfDotLocs &GetMapOfDotLocs() const { return m_dotLocsByStaff; }
    void SetMapOfDotLocs(const MapOfDotLocs &dotLocs) { m_dotLocsByStaff = dotLocs; };

    void IsAdjusted(bool isAdjusted) { m_isAdjusted = isAdjusted; }
    bool IsAdjusted() const { return m_isAdjusted; }

    //----------//
    // Functors //
    //----------//

    /**
     * Overwritten version of Save that avoids anything to be written
     */
    ///@{
    int Save(FunctorParams *functorParams) override { return FUNCTOR_CONTINUE; }
    int SaveEnd(FunctorParams *functorParams) override { return FUNCTOR_CONTINUE; }
    ///@}

    /**
     * Set/get methods for the flagShift
     */
    ///@{
    int GetFlagShift() const { return m_flagShift; }
    void SetFlagShift(int shiftVal) { m_flagShift = shiftVal; }
    ///@}

    /**
     * See Object::ResetDrawing
     */
    int ResetDrawing(FunctorParams *functorParams) override;

    /**
     * See Object::ResetHorizontalAlignment
     */
    int ResetHorizontalAlignment(FunctorParams *functorParams) override;

private:
    //
public:
    //
private:
    /**
     * A map of dot locations
     */
    MapOfDotLocs m_dotLocsByStaff;

    bool m_isAdjusted;
    int m_flagShift;
};

//----------------------------------------------------------------------------
// Flag
//----------------------------------------------------------------------------

/**
 * This class models a stem as a layer element part and has not direct MEI equivlatent.
 */
class Flag : public LayerElement {
public:
    /**
     * @name Constructors, destructors, reset and class name methods
     * Reset method resets all attribute classes
     */
    ///@{
    Flag();
    virtual ~Flag();
    void Reset() override;
    std::string GetClassName() const override { return "Flag"; }
    ///@}

    /** Override the method since alignment is required */
    bool HasToBeAligned() const override { return true; }

    wchar_t GetFlagGlyph(data_STEMDIRECTION stemDir) const;

    Point GetStemUpSE(Doc *doc, int staffSize, bool graceSize, wchar_t &code) const;
    Point GetStemDownNW(Doc *doc, int staffSize, bool graceSize, wchar_t &code) const;

    //----------//
    // Functors //
    //----------//

    /**
     * Overwritten version of Save that avoids anything to be written
     */
    ///@{
    int Save(FunctorParams *functorParams) override { return FUNCTOR_CONTINUE; }
    int SaveEnd(FunctorParams *functorParams) override { return FUNCTOR_CONTINUE; }
    ///@}

    /**
     * See Object::ResetDrawing
     */
    int ResetDrawing(FunctorParams *functorParams) override;

private:
    //
public:
    /** The number of flags to be drawn */
    int m_drawingNbFlags;

private:
};

//----------------------------------------------------------------------------
// TupletBracket
//----------------------------------------------------------------------------

/**
 * This class models a bracket as a layer element part and has not direct MEI equivlatent.
 * It is used to represent tuplet brackets.
 */
class TupletBracket : public LayerElement, public AttTupletVis {
public:
    /**
     * @name Constructors, destructors, reset and class name methods
     * Reset method resets all attribute classes
     */
    ///@{
    TupletBracket();
    virtual ~TupletBracket();
    void Reset() override;
    std::string GetClassName() const override { return "TupletBracket"; }
    ///@}

    /**
     * @name Setter and getter for darwing rel positions
     */
    ///@{
    int GetDrawingXRelLeft() { return m_drawingXRelLeft; }
    void SetDrawingXRelLeft(int drawingXRelLeft) { m_drawingXRelLeft = drawingXRelLeft; }
    int GetDrawingXRelRight() { return m_drawingXRelRight; }
    void SetDrawingXRelRight(int drawingXRelRight) { m_drawingXRelRight = drawingXRelRight; }
    ///@}

    /**
     * @name Setter and getter for darwing positions.
     * Takes into account:
     * - the position of the first and last element.
     * - the position of the beam if aligned with a beam.
     */
    ///@{
    int GetDrawingXLeft();
    int GetDrawingXRight();
    int GetDrawingYLeft();
    int GetDrawingYRight();
    ///@}

    /**
     * @name Setter and getter for the aligned num
     */
    ///@{
    TupletNum *GetAlignedNum() { return m_alignedNum; }
    void SetAlignedNum(TupletNum *alignedNum) { m_alignedNum = alignedNum; }
    ///@}

    //----------//
    // Functors //
    //----------//

    /**
     * Overwritten version of Save that avoids anything to be written
     */
    ///@{
    int Save(FunctorParams *functorParams) override { return FUNCTOR_CONTINUE; }
    int SaveEnd(FunctorParams *functorParams) override { return FUNCTOR_CONTINUE; }
    ///@}

    /**
     * See Object::ResetHorizontalAlignment
     */
    int ResetHorizontalAlignment(FunctorParams *functorParams) override;

    /**
     * See Object::ResetVerticalAlignment
     */
    int ResetVerticalAlignment(FunctorParams *functorParams) override;

private:
    //
public:
    //
private:
    /**
     * The XRel shift from the left X position.
     * The left X position is the one of the first Chord / Note / Rest in the tuplet
     */
    int m_drawingXRelLeft;
    /**
     * The XRel shift from the right X position.
     * The right X position is the one of the last Chord / Note / Rest in the tuplet
     */
    int m_drawingXRelRight;
    /** A pointer to the num with which the TupletBracket is aligned (if any) */
    TupletNum *m_alignedNum;
};

//----------------------------------------------------------------------------
// TupletNum
//----------------------------------------------------------------------------

/**
 * This class models a tuplet num as a layer element part and has not direct MEI equivlatent.
 * It is used to represent tuplet number
 */
class TupletNum : public LayerElement, public AttNumberPlacement, public AttTupletVis {
public:
    /**
     * @name Constructors, destructors, reset and class name methods
     * Reset method resets all attribute classes
     */
    ///@{
    TupletNum();
    virtual ~TupletNum();
    void Reset() override;
    std::string GetClassName() const override { return "TupletNum"; }
    ///@}

    /**
     * @name Setter and getter for darwing positions.
     * Takes into account:
     * - the position of the first and last element.
     * - the position of the bracket if aligned with a bracket.
     * - the position of the beam if aligned with a beam.
     */
    ///@{
    int GetDrawingYMid();
    int GetDrawingXMid(Doc *doc = NULL);
    ///@}

    /**
     * @name Setter and getter for the aligned bracket
     */
    ///@{
    TupletBracket *GetAlignedBracket() { return m_alignedBracket; }
    void SetAlignedBracket(TupletBracket *alignedBracket);
    ///@}

    //----------//
    // Functors //
    //----------//

    /**
     * Overwritten version of Save that avoids anything to be written
     */
    ///@{
    int Save(FunctorParams *functorParams) override { return FUNCTOR_CONTINUE; }
    int SaveEnd(FunctorParams *functorParams) override { return FUNCTOR_CONTINUE; }
    ///@}

    /**
     * See Object::ResetHorizontalAlignment
     */
    int ResetHorizontalAlignment(FunctorParams *functorParams) override;

    /**
     * See Object::ResetVerticalAlignment
     */
    int ResetVerticalAlignment(FunctorParams *functorParams) override;

private:
    //
public:
    //
private:
    /** A pointer to the bracket with which the TupletNum is aligned (if any) */
    TupletBracket *m_alignedBracket;
};

//----------------------------------------------------------------------------
// Stem
//----------------------------------------------------------------------------

/**
 * This class models a stem as a layer element part and has not direct MEI equivlatent.
 */
class Stem : public LayerElement, public AttGraced, public AttStems, public AttStemsCmn {
public:
    /**
     * @name Constructors, destructors, reset and class name methods
     * Reset method resets all attribute classes
     */
    ///@{
    Stem();
    virtual ~Stem();
    void Reset() override;
    std::string GetClassName() const override { return "Stem"; }
    ///@}

    /** Override the method since alignment is required */
    bool HasToBeAligned() const override { return true; }

    /**
     * Add an element (only flag supported) to a stem.
     */
    bool IsSupportedChild(Object *object) override;

    /**
     * @name Setter and getter for darwing stem direction and length
     */
    ///@{
    data_STEMDIRECTION GetDrawingStemDir() { return m_drawingStemDir; }
    void SetDrawingStemDir(data_STEMDIRECTION drawingStemDir) { m_drawingStemDir = drawingStemDir; }
    int GetDrawingStemLen() { return m_drawingStemLen; }
    void SetDrawingStemLen(int drawingStemLen) { m_drawingStemLen = drawingStemLen; }
    ///@}

    /**
     * @name Setter and getter of the virtual flag
     */
    ///@{
    bool IsVirtual() const { return m_isVirtual; }
    void IsVirtual(bool isVirtual) { m_isVirtual = isVirtual; }
    ///@}

    /**
     * Helper to adjust overlaping layers for stems
     */
    int CompareToElementPosition(Doc *doc, LayerElement *otherElement, int margin);

    //----------//
    // Functors //
    //----------//

    /**
     * See Object::CalcStem
     */
    int CalcStem(FunctorParams *functorParams) override;

    /**
     * Overwritten version of Save that avoids anything to be written
     */
    ///@{
    int Save(FunctorParams *functorParams) override { return FUNCTOR_CONTINUE; }
    int SaveEnd(FunctorParams *functorParams) override { return FUNCTOR_CONTINUE; }
    ///@}

    /**
     * See Object::ResetDrawing
     */
    int ResetDrawing(FunctorParams *functorParams) override;

private:
    /**
     * Addjusts flag placement and stem length if they are crossing notehead or ledger lines
     */
    void AdjustFlagPlacement(Doc *doc, Flag *flag, int staffSize, int verticalCenter, int duration);

public:
    //
private:
    /**
     * The drawing direction of the stem
     */
    data_STEMDIRECTION m_drawingStemDir;
    /**
     * The drawing length of stem
     */
    int m_drawingStemLen;
    /**
     * A flag indicating if a stem if virtual and should never be rendered.
     * Virtual stems are added to whole notes (and longer) for position calculation and
     * for supporting MEI @stem.mod
     */
    bool m_isVirtual;
};

} // namespace vrv

#endif
