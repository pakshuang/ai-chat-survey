import { useState, useEffect } from "react";

interface TypingEffectProps {
  text: string;
  typingSpeed?: number;
  scrollToBottom: () => void;
}

function TypingEffect({
  text,
  typingSpeed = 10,
  scrollToBottom,
}: TypingEffectProps) {
  const [displayText, setDisplayText] = useState("");

  useEffect(() => {
    let currentText = "";
    const typingInterval = setInterval(() => {
      if (currentText.length === text.length) {
        clearInterval(typingInterval);
      } else {
        currentText += text[currentText.length];
        setDisplayText(currentText);
      }
      scrollToBottom();
    }, typingSpeed);

    return () => clearInterval(typingInterval);
  }, [text, typingSpeed]);

  return <>{displayText}</>;
}

export default TypingEffect;
