"use client";

import {
  ActionBarPrimitive,
  AuiIf,
  AttachmentPrimitive,
  ComposerPrimitive,
  MessagePrimitive,
  ThreadPrimitive,
  useAuiState,
  useLocalRuntime,
  AssistantRuntimeProvider,
  type ChatModelAdapter,
} from "@assistant-ui/react";
import {
  ArrowUpIcon,
  AudioLines,
  BookOpen,
  Calendar as CalendarIcon,
  CheckIcon,
  ChevronDownIcon,
  ClipboardIcon,
  Code as CodeIcon,
  FolderOpen,
  GraduationCap,
  Layers,
  Menu,
  PanelLeft,
  PanelRight,
  PencilIcon,
  PenLine,
  PlusIcon,
  RefreshCwIcon,
  Sparkle,
  ThumbsDown,
  ThumbsUp,
  XIcon,
} from "lucide-react";
import { useEffect, useState, type FC } from "react";
import { create } from "zustand";
import { MarkdownText } from "@/components/assistant-ui/markdown-text";
import { ThreadListSidebar } from "@/components/assistant-ui/ThreadListSidebar";
import { CurriculumDrawer } from "@/components/assistant-ui/CurriculumDrawer";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Citation as CitationType } from "@/lib/types";
import { Citation as InlineCitationCard } from "@/components/elements/inline-citation";

interface CitationStore {
  activeCitation: CitationType | null;
  setActiveCitation: (c: CitationType | null) => void;
  selectedModel: string;
  setSelectedModel: (m: string) => void;
}

export const useCitationStore = create<CitationStore>((set) => ({
  activeCitation: null,
  setActiveCitation: (c) => set({ activeCitation: c }),
  selectedModel: "DeepSeek-V4-Flash-lje10",
  setSelectedModel: (m) => set({ selectedModel: m }),
}));

const messageActionButtonClassName =
  "flex size-8 items-center justify-center rounded-md text-[#5b5950] transition-colors hover:bg-[#1a1a18]/5 hover:text-[#1a1a18] dark:text-[#a3a098] dark:hover:bg-white/5 dark:hover:text-[#eee]";

export const Claude: FC = () => {
  const [rightSidebarOpen, setRightSidebarOpen] = useState(true);
  const [leftDrawerOpen, setLeftDrawerOpen] = useState(false);
  const [selectedLesson, setSelectedLesson] = useState<number | null>(null);
  const { activeCitation, setActiveCitation, selectedModel } = useCitationStore();

  // Custom Adapter connecting assistant-ui to Django Backend & Gemma/DeepSeek RAG
  const highSchoolChatAdapter: ChatModelAdapter = {
    async run({ messages, abortSignal }) {
      const lastUserMessage = messages
        .filter((m) => m.role === "user")
        .pop();

      const queryText =
        lastUserMessage?.content
          .filter((c) => c.type === "text")
          .map((c: any) => c.text)
          .join("\n") || "";

      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: queryText,
          message: queryText,
          lesson_number: selectedLesson,
          model: selectedModel,
        }),
        signal: abortSignal,
      });

      if (!response.ok) {
        throw new Error("خطا در برقراری ارتباط با مدل آموزشی");
      }

      const data = await response.json();
      if (data.citations && data.citations.length > 0) {
        setActiveCitation({
          lesson_number: data.citations[0].lesson_number,
          lesson_title: data.citations[0].lesson_title,
          page_start: data.citations[0].page_start,
          page_end: data.citations[0].page_end,
          section_title: data.citations[0].section_title,
          content_excerpt: data.citations[0].snippet || data.citations[0].content,
          rrf_score: data.citations[0].relevance_score,
        });
      }

      return {
        content: [
          {
            type: "text",
            text: data.answer || "پاسخی از کتاب درسی استخراج نشد.",
          },
        ],
      };
    },
  };

  const runtime = useLocalRuntime(highSchoolChatAdapter);

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <div className="flex h-screen w-full overflow-hidden bg-[#F0ECE0] text-[#1a1a18] dark:bg-[#2b2a27] dark:text-[#eee] font-sans" dir="rtl">
        {/* 1. Right Sidebar: Chat Thread List */}
        <ThreadListSidebar
          isOpen={rightSidebarOpen}
          onToggle={() => setRightSidebarOpen(!rightSidebarOpen)}
        />

        {/* 2. Center Area: Active Thread */}
        <div className="flex-1 flex flex-col h-full overflow-hidden relative">
          {/* Top Navigation Bar */}
          <header className="h-14 border-b border-[#DCD4C2]/70 dark:border-[#3B3934] px-4 flex items-center justify-between bg-[#F0ECE0]/90 backdrop-blur-xs z-10">
            <div className="flex items-center gap-2">
              {!rightSidebarOpen && (
                <button
                  onClick={() => setRightSidebarOpen(true)}
                  className="p-1.5 rounded-lg text-[#5b5950] hover:bg-[#1a1a18]/5 dark:text-[#a3a098] dark:hover:bg-white/5 transition-colors"
                  title="باز کردن لیست چت‌ها"
                >
                  <PanelRight className="size-4" />
                </button>
              )}
              <div className="flex items-center gap-1.5 text-xs font-semibold text-[#5b5950] dark:text-[#a3a098]">
                <span>فیلتر مبحث:</span>
                <button
                  onClick={() => setLeftDrawerOpen(true)}
                  className="bg-white/80 dark:bg-[#1f1e1b] border border-[#DCD4C2] dark:border-[#3B3934] px-2.5 py-1 rounded-lg text-xs font-medium text-[#1a1a18] dark:text-[#eee] hover:bg-white transition-all flex items-center gap-1"
                >
                  <BookOpen className="size-3 text-[#c96442]" />
                  <span>{selectedLesson ? `درس ${selectedLesson}` : "همه ۱۰ درس (کل کتاب)"}</span>
                </button>
              </div>
            </div>

            {/* Left Header Tools */}
            <div className="flex items-center gap-2">
              <button
                onClick={() => setLeftDrawerOpen(true)}
                className="flex items-center gap-1.5 bg-[#EAE4D3] dark:bg-[#252420] border border-[#DCD4C2] dark:border-[#3B3934] px-3 py-1.5 rounded-xl text-xs font-serif font-semibold text-[#1a1a18] dark:text-[#eee] hover:bg-white/60 transition-all shadow-2xs"
                title="مشاهده سرفصل‌های کتاب دین و زندگی"
              >
                <Layers className="size-3.5 text-[#c96442]" />
                <span className="hidden sm:inline">سرفصل‌های کتاب درسی</span>
              </button>
            </div>
          </header>

          {/* Main Thread Content */}
          <ThreadPrimitive.Root className="flex flex-1 flex-col items-stretch overflow-hidden">
            <AuiIf condition={(s) => s.thread.isEmpty}>
              <EmptyState onOpenCurriculum={() => setLeftDrawerOpen(true)} />
            </AuiIf>

            <AuiIf condition={(s) => !s.thread.isEmpty}>
              <ThreadPrimitive.Viewport className="flex grow flex-col overflow-y-auto px-4 pt-6">
                <ThreadPrimitive.Messages>
                  {() => <ChatMessage />}
                </ThreadPrimitive.Messages>

                <ThreadPrimitive.ViewportFooter className="sticky bottom-0 mx-auto mt-auto w-full max-w-3xl bg-linear-to-b from-transparent via-[#F0ECE0]/85 to-[#F0ECE0] pt-4 pb-2 dark:via-[#2b2a27]/85 dark:to-[#2b2a27]">
                  <Composer />
                  <p className="pt-2 text-center text-xs text-[#8a8780] dark:text-[#a3a098]">
                    پاسخ‌ها مستند به کتاب دین و زندگی ۳ و کلید امتحانات نهایی با مدل هوشمند {selectedModel} تولید می‌شوند.
                  </p>
                </ThreadPrimitive.ViewportFooter>
              </ThreadPrimitive.Viewport>
            </AuiIf>
          </ThreadPrimitive.Root>
        </div>

        {/* 3. Left Drawer: Curriculum Chapters & Active Citation */}
        <CurriculumDrawer
          isOpen={leftDrawerOpen}
          onClose={() => setLeftDrawerOpen(false)}
          selectedLesson={selectedLesson}
          onSelectLesson={(num) => {
            setSelectedLesson(num);
            setLeftDrawerOpen(false);
          }}
          activeCitation={activeCitation}
        />
      </div>
    </AssistantRuntimeProvider>
  );
};

const EmptyState: FC<{ onOpenCurriculum: () => void }> = ({ onOpenCurriculum }) => {
  return (
    <div className="flex grow flex-col items-center justify-center px-4 py-8">
      <div className="mx-auto flex w-full max-w-2xl flex-col items-stretch gap-5">
        <h1 className="flex items-center justify-center gap-3 font-serif text-3xl text-[#1a1a18] sm:text-4xl dark:text-[#eee]">
          <Sparkle className="size-7 fill-[#c96442] text-[#c96442]" />
          <span>امروز چه مبحثی را مرور کنیم؟</span>
        </h1>
        <Composer />
        <ModeTabs onOpenCurriculum={onOpenCurriculum} />
      </div>
    </div>
  );
};

const Composer: FC = () => {
  return (
    <ComposerPrimitive.Root className="flex w-full flex-col gap-2 rounded-2xl border border-[#E5E0D6] bg-white px-3.5 pt-3 pb-2.5 shadow-sm dark:border-[#3d3a35] dark:bg-[#1f1e1b]">
      <ComposerPrimitive.Input
        placeholder="سوال یا مبحث درسی خود را بپرسید..."
        rows={1}
        className="block max-h-72 min-h-6 w-full resize-none bg-transparent text-[#1a1a18] outline-none placeholder:text-[#9a9893] dark:text-[#eee] dark:placeholder:text-[#9a9893] text-sm font-sans"
      />

      <div className="flex w-full items-center gap-2">
        <ComposerPrimitive.AddAttachment
          aria-label="Add attachment"
          className="flex size-8 shrink-0 items-center justify-center rounded-md text-[#5b5950] transition-colors hover:bg-[#1a1a18]/5 hover:text-[#1a1a18] dark:text-[#a3a098] dark:hover:bg-white/5 dark:hover:text-[#eee]"
        >
          <PlusIcon width={16} height={16} />
        </ComposerPrimitive.AddAttachment>

        <div className="mr-auto flex items-center gap-1">
          <ClaudeModelPicker />
          <ComposerPrimaryAction />
        </div>
      </div>

      <AuiIf condition={(s) => s.composer.attachments.length > 0}>
        <div className="-mx-1 -mb-1 flex flex-row gap-2 overflow-x-auto pt-1">
          <ComposerPrimitive.Attachments>
            {() => <ClaudeAttachment />}
          </ComposerPrimitive.Attachments>
        </div>
      </AuiIf>
    </ComposerPrimitive.Root>
  );
};

const ComposerPrimaryAction: FC = () => {
  return (
    <>
      <AuiIf condition={(s) => s.thread.isRunning}>
        <ComposerPrimitive.Cancel className="flex size-8 items-center justify-center rounded-md bg-[#c96442] text-white transition-colors hover:bg-[#b1573a]">
          <div className="size-2.5 rounded-[2px] bg-current" />
        </ComposerPrimitive.Cancel>
      </AuiIf>

      <AuiIf
        condition={(s) => !s.thread.isRunning && s.composer.dictation != null}
      >
        <ComposerPrimitive.StopDictation
          className="flex size-8 items-center justify-center rounded-md bg-[#c96442] text-white transition-colors hover:bg-[#b1573a]"
          aria-label="Stop dictation"
        >
          <div className="size-2.5 animate-pulse rounded-[2px] bg-current" />
        </ComposerPrimitive.StopDictation>
      </AuiIf>

      <AuiIf
        condition={(s) =>
          !s.thread.isRunning &&
          s.composer.dictation == null &&
          !s.composer.isEmpty
        }
      >
        <ComposerPrimitive.Send className="flex size-8 items-center justify-center rounded-md bg-[#c96442] text-white transition-colors hover:bg-[#b1573a] disabled:pointer-events-none disabled:opacity-50">
          <ArrowUpIcon width={16} height={16} />
        </ComposerPrimitive.Send>
      </AuiIf>

      <AuiIf
        condition={(s) =>
          !s.thread.isRunning &&
          s.composer.dictation == null &&
          s.composer.isEmpty
        }
      >
        <ComposerPrimitive.Dictate
          className="flex size-8 items-center justify-center rounded-md text-[#5b5950] transition-colors hover:bg-[#1a1a18]/5 hover:text-[#1a1a18] dark:text-[#a3a098] dark:hover:bg-white/5 dark:hover:text-[#eee]"
          aria-label="Use voice mode"
        >
          <AudioLines className="size-4" />
        </ComposerPrimitive.Dictate>
      </AuiIf>
    </>
  );
};

const CLAUDE_MODELS = [
  {
    id: "DeepSeek-V4-Flash-lje10",
    name: "DeepSeek-V4-Flash",
    description: "گیت‌وی آروان‌کلود (سریع و هوشمند)",
  },
  {
    id: "gemma_4",
    name: "gemma_4 (RAG)",
    description: "مستند به کتاب درسی و نهایی",
  },
  {
    id: "bge-m3",
    name: "BGE-M3 Embedder",
    description: "پایگاه برداری PostgreSQL 16",
  },
];

const ClaudeModelPicker: FC = () => {
  const { selectedModel, setSelectedModel } = useCitationStore();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger className="flex h-8 items-center gap-1 rounded-md px-2.5 text-xs whitespace-nowrap text-[#1a1a18] transition hover:bg-[#1a1a18]/5 dark:text-[#eee] dark:hover:bg-white/5 font-serif font-medium">
        <span>{CLAUDE_MODELS.find((m) => m.id === selectedModel)?.name || selectedModel}</span>
        <ChevronDownIcon width={14} height={14} className="opacity-60" />
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="min-w-64">
        {CLAUDE_MODELS.map((m) => (
          <DropdownMenuItem
            key={m.id}
            onClick={() => setSelectedModel(m.id)}
            className="flex items-start gap-2.5 p-2 cursor-pointer"
          >
            <span className="mt-0.5 flex size-4 items-center justify-center text-[#c96442]">
              {m.id === selectedModel ? <CheckIcon className="size-3.5" /> : null}
            </span>
            <span className="flex flex-1 flex-col">
              <span className="text-foreground font-serif text-xs font-semibold">
                {m.name}
              </span>
              <span className="text-muted-foreground text-[10px]">
                {m.description}
              </span>
            </span>
          </DropdownMenuItem>
        ))}
        <DropdownMenuSeparator />
        <DropdownMenuItem className="text-muted-foreground text-xs">
          پایگاه برداری: PostgreSQL + pgvector
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};

const ModeTabs: FC<{ onOpenCurriculum: () => void }> = ({ onOpenCurriculum }) => {
  const tabs = [
    { label: "سنت‌های الهی", Icon: Sparkle },
    { label: "مراتب توحید", Icon: GraduationCap },
    { label: "پیام آیات", Icon: PenLine },
    { label: "توبه نصوح", Icon: FolderOpen },
    { label: "سرفصل‌های کتاب", Icon: CalendarIcon, onClick: onOpenCurriculum },
  ];

  return (
    <div className="flex flex-wrap items-center justify-center gap-2">
      {tabs.map(({ label, Icon, onClick }) => (
        <button
          key={label}
          type="button"
          onClick={onClick}
          className="flex h-8 items-center gap-1.5 rounded-lg border border-[#E5E0D6] bg-transparent px-3 text-xs whitespace-nowrap text-[#3d3a35] transition-colors hover:bg-white/60 dark:border-[#3d3a35] dark:text-[#cdc9be] dark:hover:bg-[#1f1e1b]/60 shadow-2xs font-serif font-medium"
        >
          <Icon className="size-3.5 text-[#8a8780] dark:text-[#a3a098]" />
          <span>{label}</span>
        </button>
      ))}
    </div>
  );
};

const ChatMessage: FC = () => {
  const { activeCitation } = useCitationStore();

  return (
    <MessagePrimitive.Root className="group/message relative mx-auto flex w-full max-w-3xl flex-col py-3 font-sans">
      <AuiIf condition={(s) => s.message.role === "user"}>
        <div className="flex flex-col items-start gap-1">
          <div className="max-w-[85%] rounded-2xl bg-[#E5E0D6] px-4 py-2.5 text-sm wrap-break-word whitespace-pre-wrap text-[#1a1a18] dark:bg-[#393937] dark:text-[#eee]">
            <MessagePrimitive.Parts>
              {({ part }) => {
                if (part.type === "text") return <MarkdownText />;
                return null;
              }}
            </MessagePrimitive.Parts>
          </div>
          <ActionBarPrimitive.Root className="-mt-px flex items-center gap-0.5 opacity-0 transition-opacity group-focus-within/message:opacity-100 group-hover/message:opacity-100">
            <ActionBarPrimitive.Edit className={messageActionButtonClassName}>
              <PencilIcon width={14} height={14} />
            </ActionBarPrimitive.Edit>
            <ActionBarPrimitive.Copy className={messageActionButtonClassName}>
              <AuiIf condition={(s) => s.message.isCopied}>
                <CheckIcon className="size-3.5 text-emerald-600" />
              </AuiIf>
              <AuiIf condition={(s) => !s.message.isCopied}>
                <ClipboardIcon width={14} height={14} />
              </AuiIf>
            </ActionBarPrimitive.Copy>
          </ActionBarPrimitive.Root>
        </div>
      </AuiIf>

      <AuiIf condition={(s) => s.message.role === "assistant"}>
        <div className="flex flex-col gap-2">
          <div className="prose prose-claude font-sans text-sm leading-[1.8rem] wrap-break-word text-[#1a1a18] dark:text-[#eee]">
            <MessagePrimitive.Parts>
              {({ part }) => {
                if (part.type === "text") return <MarkdownText />;
                return null;
              }}
            </MessagePrimitive.Parts>
          </div>

          {/* Interactive Numbered Inline Citation Card */}
          {activeCitation && (
            <div className="inline-flex items-center gap-1.5 self-start mt-1 bg-white/70 dark:bg-[#1f1e1b] border border-[#DCD4C2] dark:border-[#3B3934] px-2.5 py-1 rounded-xl shadow-2xs">
              <span className="text-[11px] text-[#8a8780] dark:text-[#a3a098] font-medium">مرجع کتاب درسی:</span>
              <InlineCitationCard
                index={0}
                source={{
                  domain: "کتاب دین و زندگی ۳",
                  title: `درس ${activeCitation.lesson_number}: ${activeCitation.lesson_title}`,
                  snippet: activeCitation.content_excerpt || "متن استخراج‌شده از کتاب درسی رسمی",
                  page_number: activeCitation.page_start,
                  lesson_number: activeCitation.lesson_number,
                }}
              />
            </div>
          )}

          <ActionBarPrimitive.Root className="mt-1 flex items-center gap-0.5 opacity-0 transition-opacity group-focus-within/message:opacity-100 group-hover/message:opacity-100">
            <ActionBarPrimitive.Copy className={messageActionButtonClassName}>
              <AuiIf condition={(s) => s.message.isCopied}>
                <CheckIcon className="size-3.5 text-emerald-600" />
              </AuiIf>
              <AuiIf condition={(s) => !s.message.isCopied}>
                <ClipboardIcon width={14} height={14} />
              </AuiIf>
            </ActionBarPrimitive.Copy>
            <ActionBarPrimitive.FeedbackPositive
              className={messageActionButtonClassName}
            >
              <ThumbsUp className="size-3.5" />
            </ActionBarPrimitive.FeedbackPositive>
            <ActionBarPrimitive.FeedbackNegative
              className={messageActionButtonClassName}
            >
              <ThumbsDown className="size-3.5" />
            </ActionBarPrimitive.FeedbackNegative>
            <ActionBarPrimitive.Reload className={messageActionButtonClassName}>
              <RefreshCwIcon width={14} height={14} />
            </ActionBarPrimitive.Reload>
          </ActionBarPrimitive.Root>
        </div>
      </AuiIf>
    </MessagePrimitive.Root>
  );
};

const useFileSrc = (file: File | undefined) => {
  const [src, setSrc] = useState<string | undefined>(undefined);

  useEffect(() => {
    if (!file) {
      setSrc(undefined);
      return;
    }

    const objectUrl = URL.createObjectURL(file);
    setSrc(objectUrl);

    return () => {
      URL.revokeObjectURL(objectUrl);
    };
  }, [file]);

  return src;
};

const useAttachmentSrc = () => {
  const file = useAuiState((s: any) => s?.attachment?.file);
  const src = useAuiState((s: any) => s?.attachment?.content?.filter((c: any) => c.type === "image")[0]?.image);
  return useFileSrc(file) ?? src;
};

const ClaudeAttachment: FC = () => {
  const isImage = useAuiState((s: any) => s?.attachment?.type === "image");
  const src = useAttachmentSrc();

  return (
    <AttachmentPrimitive.Root className="group/thumbnail relative">
      <div
        className="overflow-hidden rounded-lg border border-[#E5E0D6] dark:border-[#3d3a35]"
        style={{ width: "80px", height: "80px" }}
      >
        {isImage && src ? (
          <img
            className="h-full w-full object-cover"
            alt="Attachment"
            src={src}
          />
        ) : (
          <div className="flex h-full w-full items-center justify-center bg-white text-[#5b5950] dark:bg-[#2b2a27] dark:text-[#a3a098]">
            <AttachmentPrimitive.unstable_Thumb className="text-xs" />
          </div>
        )}
      </div>
      <AttachmentPrimitive.Remove
        className="absolute -top-1.5 -right-1.5 flex size-5 items-center justify-center rounded-full bg-[#1a1a18] text-white opacity-0 transition-opacity group-focus-within/thumbnail:opacity-100 group-hover/thumbnail:opacity-100 hover:bg-[#3d3a35] dark:bg-white dark:text-[#1a1a18] dark:hover:bg-[#cdc9be]"
        aria-label="Remove attachment"
      >
        <XIcon width={12} height={12} />
      </AttachmentPrimitive.Remove>
    </AttachmentPrimitive.Root>
  );
};
