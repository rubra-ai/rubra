import React, { useEffect } from 'react';

export default function GradioApp() {
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://gradio.s3-us-west-2.amazonaws.com/4.36.1/gradio.js';
    script.async = true;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  return <gradio-app src="https://gokaygokay-florence-2.hf.space"></gradio-app>;
}