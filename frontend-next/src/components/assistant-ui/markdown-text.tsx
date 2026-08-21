"use client";

import React, { FC } from "react";
import { MessagePrimitive } from "@assistant-ui/react";

export const MarkdownText: FC<{ sources?: any[] }> = () => {
  return (
    <div className="leading-relaxed whitespace-pre-wrap font-sans text-sm">
      <MessagePrimitive.Content />
    </div>
  );
};
