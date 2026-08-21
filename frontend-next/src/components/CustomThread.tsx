"use client";

import React, { useState, useRef, useEffect } from "react";
import { Send, GraduationCap, User, Sparkles, BookOpen, AlertCircle } from "lucide-react";
import { Citation, ExamQuestion } from "@/lib/types";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  citation?: Citation;
}

interface CustomThreadProps {
  selectedLesson: number | null;
  onCitationUpdate: (citation: Citation | null) => void;
  onExamQuestionsUpdate: (questions: ExamQuestion[]) => void;
}

const QUICK_PROMPTS = [
  { text: "سنت ابتلا و آزمایش", prompt: "سنت ابتلا و آزمایش الهی به چه معناست و چه اهدافی دارد؟" },
  { text: "مراتب توحید", prompt: "مراتب توحید چیست و توحید در خالقیت و ربوبیت چه تفاوتی دارند؟" },
  { text: "توبه نصوح (درس ۷)", prompt: "توبه نصوح یعنی چه و چه شرایطی برای قبولی توبه در قرآن ذکر شده؟" },
  { text: "پیام آیه ۱۵ سوره فاطر", prompt: "پیام و مفهوم آیه یا ایها الناس انتم الفقراء الی الله چیست؟" },
];

export const CustomThread: React.FC<CustomThreadProps> = ({
  selectedLesson,
  onCitationUpdate,
  onExamQuestionsUpdate,
}) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "سلام! من دستیار هوشمند آموزشی دین و زندگی ۳ (پایه دوازدهم) هستم. تمام پاسخ‌های من بر اساس متن رسمی کتاب درسی و بارم‌بندی امتحانات نهایی استخراج و ارجاع داده می‌شوند. سوال یا مبحث خود را مطرح کنید.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSubmit = async (textToSend?: string) => {
    const query = textToSend || input.trim();
    if (!query || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: query,
    };

    setMessages((prev) => [...prev, userMessage]);
    if (!textToSend) setInput("");
    setLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: query,
          lesson_number: selectedLesson,
        }),
      });

      if (!response.ok) {
        throw new Error("خطا در برقراری ارتباط با سرور");
      }

      const data = await response.json();
      
      const primaryCitation: Citation | undefined = data.citations && data.citations.length > 0 ? {
        lesson_number: data.citations[0].lesson_number,
        lesson_title: data.citations[0].lesson_title,
        page_start: data.citations[0].page_start,
        page_end: data.citations[0].page_end,
        section_title: data.citations[0].section_title,
        content_excerpt: data.citations[0].content_excerpt || data.citations[0].content,
        rrf_score: data.citations[0].rrf_score,
      } : undefined;

      if (primaryCitation) {
        onCitationUpdate(primaryCitation);
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.answer || "پاسخی دریافت نشد.",
        citation: primaryCitation,
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // If lesson citations returned, fetch relevant exam questions
      if (primaryCitation?.lesson_number) {
        try {
          const examRes = await fetch(`/django-api/exams/questions/?lesson=${primaryCitation.lesson_number}`);
          if (examRes.ok) {
            const examData = await examRes.json();
            if (Array.isArray(examData) && examData.length > 0) {
              onExamQuestionsUpdate(examData);
            }
          }
        } catch (e) {
          console.warn("Could not fetch exam questions:", e);
        }
      }
    } catch (error: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: `⚠️ متاسفانه در دریافت پاسخ خطایی رخ داد: ${error.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[750px] bg-white rounded-2xl shadow-sm border border-slate-200/80 overflow-hidden">
      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-3.5 ${
              msg.role === "user" ? "flex-row-reverse" : "flex-row"
            }`}
          >
            {/* Avatar */}
            <div
              className={`w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 ${
                msg.role === "user"
                  ? "bg-indigo-600 text-white"
                  : "bg-emerald-600 text-white"
              }`}
            >
              {msg.role === "user" ? (
                <User className="w-5 h-5" />
              ) : (
                <GraduationCap className="w-5 h-5" />
              )}
            </div>

            {/* Bubble */}
            <div
              className={`max-w-[85%] rounded-2xl px-5 py-4 text-sm leading-relaxed ${
                msg.role === "user"
                  ? "bg-indigo-600 text-white rounded-tr-none"
                  : "bg-slate-50 text-slate-800 border border-slate-200/70 rounded-tl-none"
              }`}
            >
              <div className="whitespace-pre-line">{msg.content}</div>

              {msg.citation && (
                <div className="mt-3 pt-2.5 border-t border-slate-200/80 flex items-center gap-2 text-xs font-semibold text-emerald-800">
                  <BookOpen className="w-3.5 h-3.5" />
                  <span>
                    مرجع رسمی: درس {msg.citation.lesson_number}، صفحه{" "}
                    {msg.citation.page_start}
                  </span>
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex gap-3.5 items-center text-slate-400 text-xs">
            <div className="w-9 h-9 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
              <GraduationCap className="w-5 h-5 animate-pulse" />
            </div>
            <div className="bg-slate-50 border border-slate-200/70 rounded-2xl px-4 py-3 text-slate-500 flex items-center gap-2">
              <span className="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
              <span>در حال جستجوی کانونیکال و استخراج پاسخ از کتاب درسی...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompts */}
      <div className="px-6 py-2.5 bg-slate-50/50 border-t border-slate-100 flex flex-wrap gap-2 items-center">
        <span className="text-[11px] font-bold text-slate-400 flex items-center gap-1">
          <Sparkles className="w-3 h-3 text-amber-500" />
          پیشنهاد سریع:
        </span>
        {QUICK_PROMPTS.map((qp, idx) => (
          <button
            key={idx}
            onClick={() => handleSubmit(qp.prompt)}
            disabled={loading}
            className="text-xs bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 px-2.5 py-1 rounded-full transition-colors font-medium"
          >
            {qp.text}
          </button>
        ))}
      </div>

      {/* Input Composer */}
      <div className="p-4 bg-white border-t border-slate-200/80">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSubmit();
          }}
          className="flex gap-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="سوال خود را درباره مفاهیم درس یا امتحانات نهایی بنویسید..."
            disabled={loading}
            className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-all text-slate-800"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white px-5 rounded-xl flex items-center justify-center gap-2 font-medium text-sm transition-colors shadow-sm"
          >
            <span>ارسال</span>
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
};
