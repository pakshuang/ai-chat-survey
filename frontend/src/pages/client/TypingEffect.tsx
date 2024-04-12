import { useState, useEffect } from "react";

interface TypingEffectProps {
  text: string;
  typingSpeed?: number;
}

function TypingEffect({
  text,
  typingSpeed = 10,
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
    }, typingSpeed);
    return () => clearInterval(typingInterval);
  }, [text, typingSpeed]);

  return <>{displayText}</>;
}

export default TypingEffect;
