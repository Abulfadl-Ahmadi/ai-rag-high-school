import React from "react";
import { Award, Sparkles, HelpCircle } from "lucide-react";
import { ExamQuestion } from "@/lib/types";

interface ExamIntelligenceProps {
  questions: ExamQuestion[];
  lessonNumber?: number | null;
}

export const ExamIntelligence: React.FC<ExamIntelligenceProps> = ({ questions, lessonNumber }) => {
  return (
    <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200/80">
      <div className="flex items-center gap-2 text-slate-800 font-bold text-base mb-3 border-b pb-2">
        <Award className="w-5 h-5 text-amber-500" />
        <span>هوش امتحانی و بارم‌بندی نهایی</span>
      </div>

      <div className="mb-4">
        <div className="flex items-center justify-between text-xs text-slate-600 mb-1">
          <span className="font-medium">ضریب تکرار در امتحان نهایی:</span>
          <span className="text-amber-500 font-bold">⭐⭐⭐⭐⭐</span>
        </div>
        <p className="text-xs text-slate-500 leading-relaxed">
          {lessonNumber
            ? `سوالات درس ${lessonNumber} معمولاً شامل تعاریف کلیدی، پیام آیات و تحلیل روابط علت و معلولی است.`
            : "مباحث پایه‌ای دین و زندگی ۳ هر ساله سهم ثابتی در بارم‌بندی سوالات تشریحی و کوتاه پاسخ دارند."}
        </p>
      </div>

      {questions.length > 0 ? (
        <div className="space-y-3">
          <div className="text-xs font-bold text-slate-700 flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
            <span>نمونه سوالات نهایی سال‌های قبل:</span>
          </div>
          {questions.slice(0, 2).map((q) => (
            <div key={q.id} className="bg-slate-50 rounded-xl p-3 border border-slate-100 text-xs">
              <div className="flex justify-between items-center text-slate-500 font-semibold mb-1 text-[11px]">
                <span>نهایی {q.exam_session} {q.exam_year}</span>
                <span className="text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded">{q.score} نمره</span>
              </div>
              <p className="text-slate-800 mb-2 font-medium">«{q.question_text}»</p>
              {q.answer_key?.ideal_response && (
                <div className="bg-emerald-50/50 p-2 rounded-lg border border-emerald-100 text-[11px] text-emerald-950">
                  <span className="font-bold text-emerald-800 block mb-0.5">کلید مصحح:</span>
                  {q.answer_key.ideal_response}
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-slate-50 rounded-xl p-3 text-center text-xs text-slate-400">
          <HelpCircle className="w-4 h-4 mx-auto mb-1 text-slate-300" />
          نمونه سوالات امتحانات نهایی با انتخاب درس یا طرح پرسش بارگذاری می‌شوند.
        </div>
      )}
    </div>
  );
};
