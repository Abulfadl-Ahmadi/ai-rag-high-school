"use client";

import React, { FC, useState } from "react";
import {
  ThreadListPrimitive,
  ThreadListItemPrimitive,
  ThreadListItemMorePrimitive,
} from "@assistant-ui/react";
import {
  ArchiveIcon,
  Bot,
  CheckIcon,
  GraduationCap,
  MessageSquarePlus,
  MoreHorizontalIcon,
  PanelRight,
  PlusIcon,
  Search,
  Sparkles,
  TrashIcon,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface ThreadListSidebarProps {
  isOpen: boolean;
  onToggle: () => void;
}

export const ThreadListSidebar: FC<ThreadListSidebarProps> = ({
  isOpen,
  onToggle,
}) => {
  const [searchTerm, setSearchTerm] = useState("");

  return (
    <aside
      className={cn(
        "flex flex-col border-l border-[#DCD4C2] bg-[#EAE4D3] transition-all duration-300 z-20 shrink-0 dark:border-[#3B3934] dark:bg-[#252420]",
        isOpen ? "w-72" : "w-0 overflow-hidden border-none"
      )}
    >
      {/* Brand Header */}
      <div className="flex h-14 items-center justify-between px-4 border-b border-[#DCD4C2]/60 dark:border-[#3B3934]">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-[#c96442] flex items-center justify-center text-white shadow-sm">
            <GraduationCap className="size-5" />
          </div>
          <div>
            <div className="font-serif font-bold text-sm text-[#1a1a18] dark:text-[#eee]">دبیرستان هوشمند</div>
            <div className="text-[10px] text-[#8a8780] dark:text-[#a3a098]">دین و زندگی ۳ (پایه ۱۲)</div>
          </div>
        </div>
        <button
          onClick={onToggle}
          className="p-1.5 rounded-lg text-[#5b5950] hover:bg-[#1a1a18]/5 dark:text-[#a3a098] dark:hover:bg-white/5 transition-colors"
          title="بستن لیست چت‌ها"
        >
          <PanelRight className="size-4" />
        </button>
      </div>

      {/* ThreadList Primitive Container */}
      <ThreadListPrimitive.Root className="flex flex-col flex-1 overflow-hidden p-3 gap-2">
        {/* New Thread Button */}
        <ThreadListPrimitive.New asChild>
          <button className="flex w-full items-center justify-center gap-2 rounded-xl bg-white/90 dark:bg-[#1f1e1b] border border-[#DCD4C2] dark:border-[#3B3934] px-4 py-2.5 text-xs font-serif font-semibold text-[#1a1a18] dark:text-[#eee] shadow-xs hover:bg-white transition-all">
            <PlusIcon className="size-4 text-[#c96442]" />
            <span>گفتگوی جدید (New Chat)</span>
          </button>
        </ThreadListPrimitive.New>

        {/* Search Threads */}
        <div className="relative mt-1 mb-1">
          <Search className="size-3.5 absolute right-2.5 top-1/2 -translate-y-1/2 text-[#8a8780]" />
          <input
            type="text"
            placeholder="جستجوی گفتگوها..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-white/60 dark:bg-[#1f1e1b]/60 border border-[#DCD4C2]/80 dark:border-[#3B3934] rounded-lg pr-8 pl-2.5 py-1.5 text-xs text-[#1a1a18] dark:text-[#eee] placeholder:text-[#9a9893] outline-none focus:bg-white dark:focus:bg-[#1f1e1b] transition-all"
          />
        </div>

        {/* Threads List Items */}
        <div className="flex-1 overflow-y-auto space-y-1 pr-0.5">
          <div className="px-1 py-1 text-[11px] font-bold text-[#8a8780] dark:text-[#a3a098] uppercase tracking-wider flex items-center justify-between">
            <span>تاریخچه گفتگوها</span>
            <span className="text-[10px] font-mono text-[#8a8780]">RAG</span>
          </div>

          <ThreadListPrimitive.Items>
            {() => (
              <ThreadListItemPrimitive.Root className="group relative flex h-9 items-center rounded-xl px-2.5 text-xs text-[#3d3a35] dark:text-[#cdc9be] hover:bg-white/80 dark:hover:bg-[#1f1e1b] data-active:bg-white dark:data-active:bg-[#1f1e1b] data-active:shadow-xs data-active:text-[#1a1a18] dark:data-active:text-[#eee] transition-all cursor-pointer">
                <ThreadListItemPrimitive.Trigger className="min-w-0 flex-1 truncate text-right outline-none">
                  <ThreadListItemPrimitive.Title fallback="گفتگوی جدید" />
                </ThreadListItemPrimitive.Trigger>

                <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  <ThreadListItemPrimitive.Archive asChild>
                    <button
                      className="p-1 hover:text-[#c96442] transition-colors"
                      title="آرشیو"
                    >
                      <ArchiveIcon className="size-3" />
                    </button>
                  </ThreadListItemPrimitive.Archive>
                  <ThreadListItemPrimitive.Delete asChild>
                    <button
                      className="p-1 hover:text-red-600 transition-colors"
                      title="حذف"
                    >
                      <TrashIcon className="size-3" />
                    </button>
                  </ThreadListItemPrimitive.Delete>
                </div>
              </ThreadListItemPrimitive.Root>
            )}
          </ThreadListPrimitive.Items>
        </div>

        {/* Footer Info */}
        <div className="pt-2 border-t border-[#DCD4C2]/60 dark:border-[#3B3934] text-[10px] text-[#8a8780] flex items-center justify-between px-1">
          <span className="flex items-center gap-1">
            <Bot className="size-3 text-[#c96442]" />
            مدل: gemma_4
          </span>
          <span className="font-mono text-[9px]">PostgreSQL 16</span>
        </div>
      </ThreadListPrimitive.Root>
    </aside>
  );
};
