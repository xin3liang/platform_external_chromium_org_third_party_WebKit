/*
 * Copyright (C) 2013 Apple Inc. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY APPLE INC. AND ITS CONTRIBUTORS ``AS IS''
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL APPLE INC. OR ITS CONTRIBUTORS
 * BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef MediaKeys_h
#define MediaKeys_h

#include "bindings/core/v8/ScriptPromise.h"
#include "bindings/core/v8/ScriptWrappable.h"
#include "core/dom/ContextLifecycleObserver.h"
#include "wtf/Forward.h"
#include "wtf/text/WTFString.h"

namespace blink {
class WebContentDecryptionModule;
}

namespace blink {

class ExceptionState;
class ExecutionContext;
class HTMLMediaElement;
class ScriptState;

// References are held by JS and HTMLMediaElement.
// The WebContentDecryptionModule has the same lifetime as this object.
class MediaKeys : public GarbageCollectedFinalized<MediaKeys>, public ContextLifecycleObserver, public ScriptWrappable {
public:
    static ScriptPromise create(ScriptState*, const String& keySystem);
    virtual ~MediaKeys();

    const String& keySystem() const { return m_keySystem; }

    ScriptPromise createSession(ScriptState*, const String& initDataType, ArrayBuffer* initData, const String& sessionType);
    ScriptPromise createSession(ScriptState*, const String& initDataType, ArrayBufferView* initData, const String& sessionType);

    static bool isTypeSupported(const String& keySystem, const String& contentType);

    blink::WebContentDecryptionModule* contentDecryptionModule();

    void trace(Visitor*);

    // ContextLifecycleObserver
    virtual void contextDestroyed() OVERRIDE;

private:
    friend class MediaKeysInitializer;
    MediaKeys(ExecutionContext*, const String& keySystem, PassOwnPtr<blink::WebContentDecryptionModule>);

    ScriptPromise createSessionInternal(ScriptState*, const String& initDataType, PassRefPtr<ArrayBuffer> initData, const String& sessionType);

    const String m_keySystem;
    OwnPtr<blink::WebContentDecryptionModule> m_cdm;
};

}

#endif // MediaKeys_h
