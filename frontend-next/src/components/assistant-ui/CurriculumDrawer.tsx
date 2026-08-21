"use client";

import React, { FC } from "react";
import {
  BookOpen,
  CheckCircle2,
  ChevronLeft,
  Filter,
  GraduationCap,
  Layers,
  Sparkles,
  X,
} from "lucide-react";
import { Citation, Lesson } from "@/lib/types";
import { cn } from "@/lib/utils";

interface CurriculumDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  selectedLesson: number | null;
  onSelectLesson: (lessonNum: number | null) => void;
  activeCitation?: Citation | null;
}

const LESSONS_DATA: Lesson[] = [
  { id: 1, lesson_number: 1, title: "هستی‌بخش", part: "بخش اول : تفکر و اندیشه", page_start: 8, page_end: 17 },
  { id: 2, lesson_number: 2, title: "یگانه بی‌همتا", part: "بخش اول : تفکر و اندیشه", page_start: 18, page_end: 29 },
  { id: 3, lesson_number: 3, title: "توحید و سبک زندگی", part: "بخش اول : تفکر و اندیشه", page_start: 30, page_end: 41 },
  { id: 4, lesson_number: 4, title: "فقط برای تو", part: "بخش اول : تفکر و اندیشه", page_start: 42, page_end: 51 },
  { id: 5, lesson_number: 5, title: "قدرت پرواز", part: "بخش اول : تفکر و اندیشه", page_start: 52, page_end: 63 },
  { id: 6, lesson_number: 6, title: "سنت‌های خداوند در زندگی", part: "بخش اول : تفکر و اندیشه", page_start: 64, page_end: 79 },
  { id: 7, lesson_number: 7, title: "بازگشت", part: "بخش دوم : در مسیر", page_start: 80, page_end: 93 },
  { id: 8, lesson_number: 8, title: "زندگی در دنیای امروز و عمل به احکام الهی", part: "بخش دوم : در مسیر", page_start: 94, page_end: 107 },
  { id: 9, lesson_number: 9, title: "پایه‌های استوار", part: "بخش دوم : در مسیر", page_start: 108, page_end: 125 },
  { id: 10, lesson_number: 10, title: "تمدن جدید و مسئولیت ما", part: "بخش دوم : در مسیر", page_start: 126, page_end: 142 },
];

export const CurriculumDrawer: FC<CurriculumDrawerProps> = ({
  isOpen,
  onClose,
  selectedLesson,
  onSelectLesson,
  activeCitation,
}) => {
  return (
    <>
      {/* Backdrop */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 bg-black/30 backdrop-blur-xs z-40 transition-opacity"
        />
      )}

      {/* Drawer Panel on Left Side */}
      <div
        className={cn(
          "fixed top-0 left-0 bottom-0 w-80 sm:w-96 bg-[#F8F5EE] dark:bg-[#201f1c] border-r border-[#DCD4C2] dark:border-[#3B3934] shadow-2xl z-50 flex flex-col transition-transform duration-300 ease-in-out font-sans",
          isOpen ? "translate-x-0" : "-translate-x-full"
        )}
        dir="rtl"
      >
        {/* Drawer Header */}
        <div className="flex h-14 items-center justify-between px-4 border-b border-[#DCD4C2]/70 dark:border-[#3B3934] bg-[#EAE4D3] dark:bg-[#252420]">
          <div className="flex items-center gap-2">
            <BookOpen className="size-5 text-[#c96442]" />
            <h2 className="font-serif font-bold text-sm text-[#1a1a18] dark:text-[#eee]">
              سرفصل‌های کتاب دین و زندگی ۳
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-[#5b5950] hover:bg-[#1a1a18]/5 dark:text-[#a3a098] dark:hover:bg-white/5 transition-colors"
          >
            <X className="size-4" />
          </button>
        </div>

        {/* Global Filter Reset */}
        <div className="p-3 border-b border-[#DCD4C2]/50 dark:border-[#3B3934]">
          <button
            onClick={() => onSelectLesson(null)}
            className={cn(
              "w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition-all",
              selectedLesson === null
                ? "bg-[#c96442] text-white shadow-xs"
                : "bg-white/80 dark:bg-[#2b2a27] text-[#3d3a35] dark:text-[#eee] border border-[#DCD4C2] dark:border-[#3B3934] hover:bg-white"
            )}
          >
            <span className="flex items-center gap-2">
              <Layers className="size-4" />
              همه ۱۰ درس (پرسش از کل کتاب)
            </span>
            {selectedLesson === null && <CheckCircle2 className="size-3.5" />}
          </button>
        </div>

        {/* Active Source Inspection Box */}
        {activeCitation && (
          <div className="m-3 p-3 rounded-xl bg-white dark:bg-[#2b2a27] border border-[#DCD4C2] dark:border-[#3B3934] shadow-xs text-xs">
            <div className="flex items-center justify-between text-[#c96442] font-bold mb-1">
              <span>منبع فعال پاسخ:</span>
              <span className="bg-[#EAE4D3] dark:bg-[#1f1e1b] text-[#1a1a18] dark:text-[#eee] px-2 py-0.5 rounded font-mono text-[10px]">
                درس {activeCitation.lesson_number} • ص {activeCitation.page_start}
              </span>
            </div>
            <p className="text-slate-700 dark:text-[#ccc] text-[11px] leading-relaxed line-clamp-3">
              «{activeCitation.content_excerpt}»
            </p>
          </div>
        )}

        {/* Lessons List */}
        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          <div className="text-[11px] font-bold text-[#8a8780] dark:text-[#a3a098] px-1 uppercase">
            فهرست دروس پایه دوازدهم
          </div>

          {LESSONS_DATA.map((lesson) => {
            const isSelected = selectedLesson === lesson.lesson_number;
            return (
              <div
                key={lesson.id}
                onClick={() => onSelectLesson(isSelected ? null : lesson.lesson_number)}
                className={cn(
                  "p-3 rounded-xl border transition-all cursor-pointer flex flex-col gap-1 text-xs",
                  isSelected
                    ? "bg-white dark:bg-[#2b2a27] border-[#c96442] shadow-xs"
                    : "bg-white/70 dark:bg-[#252420] border-[#DCD4C2]/70 dark:border-[#3B3934] hover:bg-white hover:border-[#DCD4C2]"
                )}
              >
                <div className="flex items-center justify-between font-bold text-[#1a1a18] dark:text-[#eee]">
                  <span>درس {lesson.lesson_number}: {lesson.title}</span>
                  <span className="text-[10px] text-[#8a8780] font-mono">
                    ص {lesson.page_start} تا {lesson.page_end}
                  </span>
                </div>
                <div className="flex items-center justify-between text-[10px] text-[#8a8780] dark:text-[#a3a098]">
                  <span>{lesson.part}</span>
                  {isSelected && (
                    <span className="text-[#c96442] font-semibold flex items-center gap-0.5">
                      <CheckCircle2 className="size-3" /> فیلتر فعال
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-[#DCD4C2]/70 dark:border-[#3B3934] bg-[#EAE4D3]/50 dark:bg-[#252420] text-center text-[10px] text-[#8a8780]">
          منطبق بر کتاب رسمی چاپ ۱۴۰۴-۱۴۰۵ و بارم‌بندی نهایی
        </div>
      </div>
    </>
  );
};
