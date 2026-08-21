import React from "react";
import { BookOpen, CheckCircle2 } from "lucide-react";
import { Citation } from "@/lib/types";

interface SourceInspectorProps {
  citation: Citation | null;
}

export const SourceInspector: React.FC<SourceInspectorProps> = ({ citation }) => {
  if (!citation) {
    return (
      <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200/80 mb-5">
        <div className="flex items-center gap-2 text-slate-700 font-bold text-base mb-3 border-b pb-2">
          <BookOpen className="w-5 h-5 text-emerald-600" />
          <span>منبع استخراجی از کتاب درسی</span>
        </div>
        <p className="text-sm text-slate-400 text-center py-6 leading-relaxed">
          پس از ارسال پرسش، پاراگراف دقیق و شماره صفحه مرجع از کتاب دین و زندگی در این بخش نمایش داده می‌شود.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200/80 mb-5 transition-all">
      <div className="flex items-center justify-between text-slate-800 font-bold text-base mb-3 border-b pb-2">
        <div className="flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-emerald-600" />
          <span>درس {citation.lesson_number}: {citation.lesson_title}</span>
        </div>
        <span className="text-xs bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full font-medium">
          صفحه {citation.page_start}
        </span>
      </div>

      <div className="bg-emerald-50/60 rounded-xl p-4 border border-emerald-100/80 mb-3">
        <div className="text-xs font-semibold text-emerald-900 mb-1.5 flex items-center gap-1">
          <span>بخش: {citation.section_title || "متن اصلی درس"}</span>
        </div>
        <p className="text-xs leading-relaxed text-slate-700 font-normal">
          «{citation.content_excerpt || "محتوای مرتبط از کتاب درسی استخراج شد."}»
        </p>
      </div>

      <div className="flex items-center justify-between text-xs text-emerald-700 font-medium">
        <span className="flex items-center gap-1">
          <CheckCircle2 className="w-3.5 h-3.5" />
          استخراج‌شده مستقیم از کتاب درسی
        </span>
        {citation.rrf_score && (
          <span className="text-[11px] text-slate-400 font-mono">
            امتیاز تطابق: {citation.rrf_score}
          </span>
        )}
      </div>
    </div>
  );
};
