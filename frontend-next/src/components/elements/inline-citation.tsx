"use client";

import React, { ComponentProps, useState } from "react";
import * as HoverCardPrimitive from "@radix-ui/react-hover-card";
import { BookOpen, CheckCircle2, FileText } from "lucide-react";
import { cn } from "@/lib/utils";
import { floating, mono } from "./surfaces";

export interface Source {
  domain: string;
  title: string;
  snippet: string;
  lesson_number?: number;
  page_number?: number;
}

interface CitationProps {
  index: number;
  source: Source;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
}

export function Citation({ index, source, open, onOpenChange }: CitationProps) {
  return (
    <HoverCardPrimitive.Root
      open={open}
      onOpenChange={onOpenChange}
      openDelay={100}
      closeDelay={150}
    >
      <HoverCardPrimitive.Trigger asChild>
        <button
          type="button"
          className={cn(
            "mx-0.5 inline-flex h-4 min-w-4 translate-y-[-2px] cursor-pointer items-center justify-center rounded-[5px] px-1.5 align-middle font-mono text-[10px] font-bold tabular-nums transition-all shadow-2xs",
            open
              ? "bg-[#c96442] text-white"
              : "bg-[#c96442]/15 text-[#c96442] hover:bg-[#c96442] hover:text-white"
          )}
        >
          {index + 1}
        </button>
      </HoverCardPrimitive.Trigger>

      <HoverCardPrimitive.Portal>
        <HoverCardPrimitive.Content
          side="top"
          sideOffset={8}
          align="center"
          className={cn(
            floating,
            "z-50 w-72 rounded-2xl p-3.5 outline-none font-sans text-right transition-all animate-in fade-in zoom-in-95 duration-150 border border-[#DCD4C2] dark:border-[#3B3934]"
          )}
          dir="rtl"
        >
          <div className="flex items-center justify-between gap-1.5 pb-2 border-b border-[#DCD4C2]/60 dark:border-[#3B3934]">
            <div className="flex items-center gap-1.5">
              <span className="bg-[#c96442]/15 text-[#c96442] flex size-4 items-center justify-center rounded text-[9px] font-bold">
                {source.domain ? source.domain[0] : "د"}
              </span>
              <span className={cn(mono, "text-[#8a8780] dark:text-[#a3a098] text-[11px] font-medium")}>
                {source.domain || "کتاب دین و زندگی ۳"}
              </span>
            </div>
            {source.page_number && (
              <span className="bg-[#EAE4D3] dark:bg-[#252420] text-[#1a1a18] dark:text-[#eee] px-1.5 py-0.5 rounded text-[10px] font-mono font-bold">
                ص {source.page_number}
              </span>
            )}
          </div>

          <p className="mt-2 text-xs leading-snug font-bold text-[#1a1a18] dark:text-[#eee] flex items-center gap-1">
            <BookOpen className="size-3.5 text-[#c96442] shrink-0" />
            <span>{source.title}</span>
          </p>

          <p className="text-[#5b5950] dark:text-[#cdc9be] mt-1.5 text-[11px] leading-relaxed bg-[#F8F5EE] dark:bg-[#201f1c] p-2 rounded-lg border border-[#DCD4C2]/50 dark:border-[#3B3934]">
            «{source.snippet}»
          </p>

          <div className="mt-2 pt-1 flex items-center justify-between text-[10px] text-emerald-700 dark:text-emerald-400 font-semibold">
            <span className="flex items-center gap-1">
              <CheckCircle2 className="size-3" />
              مرجع رسمی امتحانات نهایی
            </span>
          </div>
        </HoverCardPrimitive.Content>
      </HoverCardPrimitive.Portal>
    </HoverCardPrimitive.Root>
  );
}

export interface InlineCitationProps extends Omit<ComponentProps<"p">, "children"> {
  sources: Source[];
  openIndex?: number | null;
  onOpenIndexChange?: (index: number | null) => void;
  text?: string;
  children?: React.ReactNode;
}

export function InlineCitation({
  sources,
  openIndex = null,
  onOpenIndexChange = () => {},
  text,
  children,
  className,
  ...props
}: InlineCitationProps) {
  const [internalOpenIndex, setInternalOpenIndex] = useState<number | null>(openIndex);

  const handleOpenChange = (idx: number, isOpen: boolean) => {
    const newIdx = isOpen ? idx : null;
    setInternalOpenIndex(newIdx);
    onOpenIndexChange(newIdx);
  };

  if (!sources || sources.length === 0) {
    return (
      <div className={cn("text-[#1a1a18] dark:text-[#eee] text-sm leading-relaxed", className)} {...props}>
        {text || children}
      </div>
    );
  }

  return (
    <div
      data-slot="inline-citation"
      className={cn("text-[#1a1a18] dark:text-[#eee] text-sm leading-relaxed", className)}
      {...props}
    >
      {text || children}
      <span className="inline-flex items-center mr-1">
        {sources.map((src, idx) => (
          <Citation
            key={idx}
            index={idx}
            source={src}
            open={internalOpenIndex === idx}
            onOpenChange={(isOpen) => handleOpenChange(idx, isOpen)}
          />
        ))}
      </span>
    </div>
  );
}
