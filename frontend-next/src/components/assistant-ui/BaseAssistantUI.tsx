"use client";

import React, { useState, useRef, useEffect, FC, ReactNode } from "react";
import {
  ArrowDownIcon,
  ArrowUpIcon,
  BookOpenIcon,
  BotIcon,
  CheckIcon,
  CopyIcon,
  GraduationCapIcon,
  HelpCircleIcon,
  LayersIcon,
  LightbulbIcon,
  MenuIcon,
  MicIcon,
  PanelLeftIcon,
  PaperclipIcon,
  RefreshCwIcon,
  Share2Icon,
  SparklesIcon,
  Trash2Icon,
  UserIcon,
} from "lucide-react";
import { Citation, ExamQuestion, Lesson } from "@/lib/types";
import { cn } from "@/lib/utils";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  citation?: Citation;
  timestamp?: string;
}

interface SuggestionGroup {
  label: string;
  icon: ReactNode;
  options: { label: string; prompt: string }[];
}

const HIGH_SCHOOL_SUGGESTIONS: SuggestionGroup[] = [
  {
    label: "سنت‌های الهی",
    icon: <SparklesIcon className="size-4 text-amber-500" />,
    options: [
      {
        label: "سنت ابتلا و آزمایش",
        prompt: "سنت ابتلا و آزمایش الهی به چه معناست و چه اهدافی در زندگی انسان دارد؟",
      },
      {
        label: "سنت املاء و استدراج",
        prompt: "سنت استدراج و املاء در قرآن چگونه توصیف شده و مشمول چه کسانی می‌شود؟",
      },
      {
        label: "امداد عام و توفیق خاص",
        prompt: "تفاوت سنت امداد عام با امداد خاص (توفیق الهی) در کتاب دین و زندگی دوازدهم چیست؟",
      },
    ],
  },
  {
    label: "مراتب توحید",
    icon: <LightbulbIcon className="size-4 text-indigo-500" />,
    options: [
      {
        label: "مراتب توحید نظری",
        prompt: "مراتب توحید نظری (ذاتی، صفاتی، افعالی، در خالقیت و ربوبیت) را مقایسه کنید.",
      },
      {
        label: "توحید عملی و بندگی",
        prompt: "مقصود از توحید عملی و اجتناب از طاغوت در آیات قرآن چیست؟",
      },
      {
        label: "شرک جلی و خفی",
        prompt: "تفاوت شرک جلی و شرک خفی در دنیای امروز چیست؟",
      },
    ],
  },
  {
    label: "پیام آیات نهایی",
    icon: <BookOpenIcon className="size-4 text-emerald-500" />,
    options: [
      {
        label: "آیه ۱۵ سوره فاطر",
        prompt: "پیام و مفهوم آیه «یا ایها الناس انتم الفقراء الی الله» چیست؟",
      },
      {
        label: "آیه ۵۳ سوره زمر",
        prompt: "پیام آیه «قل یا عبادی الذین اسرفوا علی انفسهم لاتقنطوا» در درس بازگشت چیست؟",
      },
      {
        label: "آیه ۱۰ سوره رعد",
        prompt: "ارتباط آیه «ان الله لا یغیر ما بقوم حتی یغیروا ما بانفسهم» با سنت‌های الهی چیست؟",
      },
    ],
  },
  {
    label: "مسائل نوپدید و تمدن",
    icon: <LayersIcon className="size-4 text-sky-500" />,
    options: [
      {
        label: "توبه نصوح (درس ۷)",
        prompt: "توبه نصوح یعنی چه و مراحل اصلی و تکمیلی توبه در درس هفتم کدامند؟",
      },
      {
        label: "تمدن جدید و احکام الهی",
        prompt: "مسئولیت ما در مواجهه با تمدن جدید و علم و فناوری در درس دهم چیست؟",
      },
    ],
  },
];

export const BaseAssistantUI: FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [selectedLesson, setSelectedLesson] = useState<number | null>(null);
  const [expandedGroupLabel, setExpandedGroupLabel] = useState<string | null>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [activeCitation, setActiveCitation] = useState<Citation | null>(null);
  const [selectedModel, setSelectedModel] = useState("gemma_4 (Grounded RAG)");

  const viewportRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    viewportRef.current?.scrollTo({
      top: viewportRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, loading]);

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleSendMessage = async (customPrompt?: string) => {
    const text = customPrompt || input.trim();
    if (!text || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: text,
      timestamp: new Date().toLocaleTimeString("fa-IR", { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMessage]);
    if (!customPrompt) setInput("");
    setLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: text,
          message: text,
          lesson_number: selectedLesson,
        }),
      });

      if (!response.ok) {
        throw new Error("خطا در برقراری ارتباط با سرور");
      }

      const data = await response.json();
      const primaryCit: Citation | undefined =
        data.citations && data.citations.length > 0
          ? {
              lesson_number: data.citations[0].lesson_number,
              lesson_title: data.citations[0].lesson_title,
              page_start: data.citations[0].page_start,
              page_end: data.citations[0].page_end,
              section_title: data.citations[0].section_title,
              content_excerpt: data.citations[0].snippet || data.citations[0].content,
              rrf_score: data.citations[0].relevance_score,
            }
          : undefined;

      if (primaryCit) {
        setActiveCitation(primaryCit);
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.answer || "پاسخی دریافت نشد.",
        citation: primaryCit,
        timestamp: new Date().toLocaleTimeString("fa-IR", { hour: "2-digit", minute: "2-digit" }),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: `⚠️ متاسفانه در دریافت پاسخ خطایی رخ داد: ${err.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setActiveCitation(null);
    setInput("");
  };

  const isEmpty = messages.length === 0;
  const expandedGroup = HIGH_SCHOOL_SUGGESTIONS.find((g) => g.label === expandedGroupLabel);

  return (
    <div className="flex h-screen w-full bg-slate-50 overflow-hidden text-slate-900 font-sans" dir="rtl">
      {/* 1. Sidebar */}
      <aside
        className={cn(
          "bg-white border-l border-slate-200 flex flex-col transition-all duration-300 z-30 shrink-0",
          sidebarOpen ? "w-72" : "w-0 overflow-hidden border-none"
        )}
      >
        {/* Sidebar Header */}
        <div className="h-14 border-b border-slate-100 flex items-center justify-between px-4">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white shadow-sm shadow-emerald-200">
              <GraduationCapIcon className="size-5" />
            </div>
            <div>
              <div className="font-bold text-sm text-slate-800 leading-tight">دبیرستان هوشمند</div>
              <div className="text-[11px] text-emerald-700 font-medium">دین و زندگی دوازدهم</div>
            </div>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="p-1.5 hover:bg-slate-100 rounded-lg text-slate-400 hover:text-slate-600 transition-colors md:hidden"
          >
            <PanelLeftIcon className="size-4" />
          </button>
        </div>

        {/* New Chat Button */}
        <div className="p-3">
          <button
            onClick={handleNewChat}
            className="w-full flex items-center justify-center gap-2 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold py-2.5 px-4 rounded-xl shadow-sm transition-all"
          >
            <SparklesIcon className="size-3.5 text-emerald-400" />
            <span>گفتگوی جدید (New Chat)</span>
          </button>
        </div>

        {/* Lesson Filter */}
        <div className="px-3 mb-2">
          <label className="text-[11px] font-bold text-slate-500 mb-1.5 block">فیلتر مبحث / درس:</label>
          <select
            value={selectedLesson ?? "all"}
            onChange={(e) => setSelectedLesson(e.target.value === "all" ? null : parseInt(e.target.value))}
            className="w-full bg-slate-50 border border-slate-200 text-slate-700 text-xs rounded-xl px-2.5 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 font-medium"
          >
            <option value="all">همه ۱۰ درس (کل کتاب)</option>
            <option value="1">درس ۱: هستی‌بخش (ص ۸)</option>
            <option value="2">درس ۲: یگانه بی‌همتا (ص ۱۸)</option>
            <option value="3">درس ۳: توحید و سبک زندگی (ص ۳۰)</option>
            <option value="4">درس ۴: فقط برای تو (ص ۴۲)</option>
            <option value="5">درس ۵: قدرت پرواز (ص ۵۲)</option>
            <option value="6">درس ۶: سنت‌های خداوند (ص ۶۴)</option>
            <option value="7">درس ۷: بازگشت (ص ۸۰)</option>
            <option value="8">درس ۸: زندگی در دنیای امروز (ص ۹۴)</option>
            <option value="9">درس ۹: پایه‌های استوار (ص ۱۰۸)</option>
            <option value="10">درس ۱۰: تمدن جدید (ص ۱۲۶)</option>
          </select>
        </div>

        {/* Active Source Inspector */}
        <div className="flex-1 overflow-y-auto px-3 py-2 space-y-3">
          <div className="text-[11px] font-bold text-slate-400 px-1 uppercase tracking-wider">
            منبع استخراجی فعال:
          </div>
          {activeCitation ? (
            <div className="bg-emerald-50/70 border border-emerald-200/80 rounded-xl p-3 text-xs">
              <div className="flex items-center justify-between text-emerald-900 font-bold mb-1.5">
                <span>درس {activeCitation.lesson_number}: {activeCitation.lesson_title}</span>
                <span className="bg-emerald-200/70 text-emerald-900 text-[10px] px-1.5 py-0.5 rounded font-mono">
                  ص {activeCitation.page_start}
                </span>
              </div>
              <p className="text-slate-700 text-[11px] leading-relaxed line-clamp-4">
                «{activeCitation.content_excerpt}»
              </p>
            </div>
          ) : (
            <div className="bg-slate-50 border border-dashed border-slate-200 rounded-xl p-4 text-center text-xs text-slate-400">
              با طرح سوال، پاراگراف دقیق کتاب درسی در اینجا بازرسی می‌شود.
            </div>
          )}
        </div>

        {/* Sidebar Footer */}
        <div className="p-3 border-t border-slate-100 text-[11px] text-slate-400 text-center">
          دیتابیس: PostgreSQL 16 + pgvector
        </div>
      </aside>

      {/* 2. Main Chat Area */}
      <div className="flex-1 flex flex-col h-full overflow-hidden relative">
        {/* Top Header */}
        <header className="h-14 bg-white/80 backdrop-blur border-b border-slate-200/80 px-4 flex items-center justify-between shrink-0 z-10">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-slate-100 rounded-xl text-slate-600 transition-colors"
              title={sidebarOpen ? "بستن سایدبار" : "باز کردن سایدبار"}
            >
              <PanelLeftIcon className="size-4" />
            </button>
            <div className="flex items-center gap-2">
              <span className="font-bold text-sm text-slate-800">
                {selectedLesson ? `تمرکز روی درس ${selectedLesson}` : "پاسخ‌گویی جامع به کل کتاب"}
              </span>
              <span className="bg-emerald-100 text-emerald-800 text-[10px] font-bold px-2 py-0.5 rounded-full">
                نهایی ۱۴۰۴-۱۴۰۵
              </span>
            </div>
          </div>

          {/* Model Selector Pill */}
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1.5 bg-slate-100 border border-slate-200/80 px-3 py-1 rounded-full text-xs font-semibold text-slate-700 shadow-sm">
              <BotIcon className="size-3.5 text-emerald-600" />
              <span>{selectedModel}</span>
            </div>
          </div>
        </header>

        {/* Messages Viewport */}
        <div ref={viewportRef} className="flex-1 overflow-y-auto px-4 py-6 scroll-smooth">
          <div className="max-w-3xl mx-auto space-y-6">
            {/* If Empty, render Welcome Hero & Assistant-UI Suggestions */}
            {isEmpty ? (
              <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
                <div className="w-14 h-14 rounded-2xl bg-emerald-600 flex items-center justify-center text-white shadow-lg shadow-emerald-200 mb-4">
                  <GraduationCapIcon className="size-8" />
                </div>
                <h1 className="text-2xl font-extrabold text-slate-800 mb-2 tracking-tight">
                  امروز چه مبحثی از دین و زندگی ۳ را مرور کنیم؟
                </h1>
                <p className="text-sm text-slate-500 max-w-md mb-8 leading-relaxed">
                  پاسخ‌های تحلیلی و مستند، پیام آیات و نکات بارم‌بندی امتحانات نهایی با مدل هوشمند <span className="font-bold text-emerald-700">gemma_4</span>
                </p>

                {/* Suggestion Category Pills */}
                <div className="w-full max-w-xl">
                  <div className="flex flex-wrap items-center justify-center gap-2 mb-3">
                    {HIGH_SCHOOL_SUGGESTIONS.map((group) => (
                      <button
                        key={group.label}
                        onClick={() =>
                          setExpandedGroupLabel(expandedGroupLabel === group.label ? null : group.label)
                        }
                        className={cn(
                          "flex items-center gap-1.5 bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 px-3.5 py-1.5 rounded-full text-xs font-medium transition-all shadow-sm",
                          expandedGroupLabel === group.label && "bg-slate-900 text-white border-slate-900 hover:bg-slate-900"
                        )}
                      >
                        {group.icon}
                        <span>{group.label}</span>
                      </button>
                    ))}
                  </div>

                  {/* Expanded Sub-options */}
                  {expandedGroup && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 animate-in fade-in slide-in-from-top-2 duration-200">
                      {expandedGroup.options.map((opt, idx) => (
                        <button
                          key={idx}
                          onClick={() => handleSendMessage(opt.prompt)}
                          className="bg-white hover:bg-emerald-50/50 border border-slate-200 hover:border-emerald-300 text-right p-3 rounded-xl text-xs text-slate-700 transition-all group shadow-sm flex flex-col gap-1"
                        >
                          <span className="font-bold text-emerald-800 group-hover:text-emerald-900">{opt.label}</span>
                          <span className="text-slate-400 text-[11px] line-clamp-1">{opt.prompt}</span>
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ) : (
              // Message List
              messages.map((msg) => (
                <div
                  key={msg.id}
                  className={cn(
                    "flex gap-3.5 items-start",
                    msg.role === "user" ? "flex-row-reverse" : "flex-row"
                  )}
                >
                  {/* Avatar */}
                  <div
                    className={cn(
                      "w-8 h-8 rounded-xl flex items-center justify-center shrink-0 text-white shadow-sm mt-0.5",
                      msg.role === "user" ? "bg-indigo-600" : "bg-emerald-600"
                    )}
                  >
                    {msg.role === "user" ? <UserIcon className="size-4" /> : <GraduationCapIcon className="size-4" />}
                  </div>

                  {/* Message Bubble & Content */}
                  <div className="flex-1 max-w-[88%] space-y-1.5">
                    <div
                      className={cn(
                        "rounded-2xl px-5 py-4 text-sm leading-relaxed shadow-sm transition-all",
                        msg.role === "user"
                          ? "bg-slate-900 text-white rounded-tr-none mr-auto"
                          : "bg-white text-slate-800 border border-slate-200/80 rounded-tl-none ml-auto"
                      )}
                    >
                      <div className="whitespace-pre-line">{msg.content}</div>

                      {/* Citation Tag */}
                      {msg.citation && (
                        <div className="mt-3 pt-2.5 border-t border-slate-100 flex items-center justify-between text-xs font-semibold text-emerald-800">
                          <span className="flex items-center gap-1.5">
                            <BookOpenIcon className="size-3.5 text-emerald-600" />
                            مرجع کتاب درسی: درس {msg.citation.lesson_number} (صفحه {msg.citation.page_start})
                          </span>
                          {msg.citation.rrf_score && (
                            <span className="text-[10px] text-slate-400 font-mono">
                              تطابق: {Math.round(msg.citation.rrf_score)}
                            </span>
                          )}
                        </div>
                      )}
                    </div>

                    {/* Action Bar (Copy, Time) */}
                    <div
                      className={cn(
                        "flex items-center gap-2 px-1 text-[11px] text-slate-400",
                        msg.role === "user" ? "justify-end" : "justify-start"
                      )}
                    >
                      {msg.timestamp && <span>{msg.timestamp}</span>}
                      <button
                        onClick={() => handleCopy(msg.id, msg.content)}
                        className="hover:text-slate-600 transition-colors p-0.5 rounded"
                        title="کپی متن"
                      >
                        {copiedId === msg.id ? (
                          <CheckIcon className="size-3 text-emerald-600" />
                        ) : (
                          <CopyIcon className="size-3" />
                        )}
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}

            {/* Loading Indicator */}
            {loading && (
              <div className="flex gap-3.5 items-center text-slate-500 text-xs animate-in fade-in">
                <div className="w-8 h-8 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
                  <GraduationCapIcon className="size-4 animate-bounce" />
                </div>
                <div className="bg-white border border-slate-200/80 rounded-2xl px-4 py-3 shadow-sm flex items-center gap-2.5">
                  <span className="inline-block size-2 rounded-full bg-emerald-500 animate-ping" />
                  <span>مدل gemma_4 در حال تحلیل و استخراج پاسخ از کتاب درسی...</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* 3. Floating Bottom Composer (Exact assistant-ui Base style) */}
        <div className="p-4 bg-gradient-to-t from-slate-50 via-slate-50 to-transparent shrink-0">
          <div className="max-w-3xl mx-auto">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSendMessage();
              }}
              className="bg-white border border-slate-200/90 rounded-2xl shadow-md p-2 flex flex-col gap-2 focus-within:ring-2 focus-within:ring-emerald-500/20 focus-within:border-emerald-500 transition-all"
            >
              {/* Text Input */}
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSendMessage();
                  }
                }}
                rows={1}
                placeholder="سوال یا مبحث درسی خود را بنویسید (Enter برای ارسال)..."
                disabled={loading}
                className="w-full bg-transparent resize-none px-3 py-2 text-sm focus:outline-none text-slate-800 placeholder:text-slate-400 max-h-32"
              />

              {/* Action Toolbar */}
              <div className="flex items-center justify-between pt-1 border-t border-slate-100">
                <div className="flex items-center gap-1 text-slate-400">
                  <button
                    type="button"
                    className="p-1.5 hover:bg-slate-100 rounded-lg hover:text-slate-600 transition-colors"
                    title="پیوست فایل / عکس سوال"
                  >
                    <PaperclipIcon className="size-4" />
                  </button>
                  <button
                    type="button"
                    className="p-1.5 hover:bg-slate-100 rounded-lg hover:text-slate-600 transition-colors"
                    title="ورودی صوتی"
                  >
                    <MicIcon className="size-4" />
                  </button>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-[11px] text-slate-400 hidden sm:inline">Shift + Enter برای خط جدید</span>
                  <button
                    type="submit"
                    disabled={loading || !input.trim()}
                    className="bg-slate-900 hover:bg-slate-800 disabled:opacity-30 text-white size-8 rounded-xl flex items-center justify-center shadow-sm transition-all"
                  >
                    <ArrowUpIcon className="size-4" />
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};
