import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "دبیرستان هوشمند | سامانه RAG آموزشی با assistant-ui",
  description: "دستیار هوشمند و پداگوژیکال دین و زندگی پایه دوازدهم مبتنی بر امتحانات نهایی",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fa" dir="rtl">
      <head>
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css"
        />
      </head>
      <body className="bg-slate-50 text-slate-900 min-h-screen antialiased">
        {children}
      </body>
    </html>
  );
}
