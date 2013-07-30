/*
 * Copyright (C) 2012 Google Inc. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 *
 *     * Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above
 * copyright notice, this list of conditions and the following disclaimer
 * in the documentation and/or other materials provided with the
 * distribution.
 *     * Neither the name of Google Inc. nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef PasswordGeneratorButtonElement_h
#define PasswordGeneratorButtonElement_h

#include "core/html/HTMLDivElement.h"
#include "core/loader/cache/ResourcePtr.h"

namespace WebCore {

class CachedImage;
class HTMLInputElement;
class ShadowRoot;

class PasswordGeneratorButtonElement FINAL : public HTMLDivElement {
public:
    static PassRefPtr<PasswordGeneratorButtonElement> create(Document* document)
    {
        return adoptRef(new PasswordGeneratorButtonElement(document));
    }

    void decorate(HTMLInputElement*);

    virtual bool willRespondToMouseMoveEvents() OVERRIDE;
    virtual bool willRespondToMouseClickEvents() OVERRIDE;

private:
    PasswordGeneratorButtonElement(Document*);
    virtual bool isPasswordGeneratorButtonElement() const OVERRIDE { return true; }
    virtual PassRefPtr<RenderStyle> customStyleForRenderer() OVERRIDE;
    virtual RenderObject* createRenderer(RenderStyle*) OVERRIDE;
    virtual void attach(const AttachContext& = AttachContext()) OVERRIDE;
    virtual bool isMouseFocusable() const OVERRIDE { return false; }
    virtual void defaultEventHandler(Event*) OVERRIDE;

    CachedImage* imageForNormalState();
    CachedImage* imageForHoverState();

    HTMLInputElement* hostInput();
    void updateImage();

    ResourcePtr<CachedImage> m_cachedImageForNormalState;
    ResourcePtr<CachedImage> m_cachedImageForHoverState;
    bool m_isInHoverState;
};

}
#endif
