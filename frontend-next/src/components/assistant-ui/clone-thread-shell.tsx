"use client";

import React, { FC, ReactNode, useState } from "react";
import {
  GraduationCap,
  PanelLeft,
  Plus,
  BookOpen,
  Sparkles,
  Layers,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface CloneThreadShellProps {
  children: ReactNode;
  railClassName?: string;
}

export const CloneThreadShell: FC<CloneThreadShellProps> = ({
  children,
  railClassName,
}) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="flex h-screen w-full overflow-hidden bg-[#F0ECE0] text-[#1a1a18] dark:bg-[#2b2a27] dark:text-[#eee]" dir="rtl">
      {/* Sidebar Rail */}
      <aside
        className={cn(
          "flex flex-col border-l border-[#DCD4C2] bg-[#EAE4D3] transition-all duration-300 z-20 shrink-0 dark:border-[#3B3934] dark:bg-[#252420]",
          railClassName,
          sidebarOpen ? "w-64" : "w-0 overflow-hidden border-none"
        )}
      >
        {/* Brand */}
        <div className="flex h-14 items-center justify-between px-4 border-b border-[#DCD4C2]/60 dark:border-[#3B3934]">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-[#c96442] flex items-center justify-center text-white shadow-sm">
              <GraduationCap className="size-5" />
            </div>
            <div>
              <span className="font-serif font-bold text-sm text-[#1a1a18] dark:text-[#eee]">دبیرستان هوشمند</span>
              <span className="block text-[10px] text-[#8a8780] dark:text-[#a3a098]">دین و زندگی ۳ (پایه ۱۲)</span>
            </div>
          </div>
        </div>

        {/* Action Button */}
        <div className="p-3">
          <button
            onClick={() => window.location.reload()}
            className="w-full flex items-center justify-center gap-2 rounded-xl bg-white/80 dark:bg-[#1f1e1b] border border-[#DCD4C2] dark:border-[#3B3934] px-3 py-2 text-xs font-serif font-semibold text-[#1a1a18] dark:text-[#eee] shadow-xs hover:bg-white transition-all"
          >
            <Plus className="size-3.5 text-[#c96442]" />
            <span>گفتگوی جدید (New Chat)</span>
          </button>
        </div>

        {/* Quick Menu / Lessons */}
        <div className="flex-1 overflow-y-auto px-3 py-2 space-y-1">
          <div className="px-2 py-1 text-[11px] font-bold text-[#8a8780] dark:text-[#a3a098] uppercase tracking-wider">
            سرفصل‌های کتاب درسی
          </div>
          {[
            { num: 1, title: "هستی‌بخش", page: "ص ۸" },
            { num: 2, title: "یگانه بی‌همتا", page: "ص ۱۸" },
            { num: 3, title: "توحید و سبک زندگی", page: "ص ۳۰" },
            { num: 4, title: "فقط برای تو", page: "ص ۴۲" },
            { num: 5, title: "قدرت پرواز", page: "ص ۵۲" },
            { num: 6, title: "سنت‌های خداوند در زندگی", page: "ص ۶۴" },
            { num: 7, title: "بازگشت (توبه)", page: "ص ۸۰" },
            { num: 8, title: "زندگی در دنیای امروز", page: "ص ۹۴" },
            { num: 9, title: "پایه‌های استوار", page: "ص ۱۰۸" },
            { num: 10, title: "تمدن جدید و مسئولیت ما", page: "ص ۱۲۶" },
          ].map((l) => (
            <div
              key={l.num}
              className="flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs hover:bg-[#DCD4C2]/50 dark:hover:bg-[#3B3934]/50 cursor-pointer transition-colors text-[#3d3a35] dark:text-[#cdc9be]"
            >
              <span>درس {l.num}: {l.title}</span>
              <span className="text-[10px] text-[#8a8780] font-mono">{l.page}</span>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-[#DCD4C2]/60 dark:border-[#3B3934] text-[10px] text-[#8a8780] text-center">
          پایگاه داده: PostgreSQL 16 + pgvector • مدل: gemma_4
        </div>
      </aside>

      {/* Main Content Viewport */}
      <div className="flex-1 flex flex-col h-full overflow-hidden relative">
        {/* Toggle Button */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="absolute top-3 right-3 z-30 p-2 rounded-lg text-[#5b5950] hover:bg-[#1a1a18]/5 dark:text-[#a3a098] dark:hover:bg-white/5 transition-colors"
          title={sidebarOpen ? "بستن منو" : "باز کردن منو"}
        >
          <PanelLeft className="size-4" />
        </button>

        {children}
      </div>
    </div>
  );
};
