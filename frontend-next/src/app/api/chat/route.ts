import { NextRequest, NextResponse } from "next/server";

const DJANGO_BACKEND_URL = process.env.DJANGO_BACKEND_URL || "http://127.0.0.1:8000";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { message, question, lesson_number, conversation_id, model, model_name } = body;
    const queryText = question || message || "";

    const response = await fetch(`${DJANGO_BACKEND_URL}/api/chat/ask/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: queryText,
        message: queryText,
        lesson_number: lesson_number ? parseInt(lesson_number) : null,
        conversation_id: conversation_id || null,
        model: model || model_name || "DeepSeek-V4-Flash-lje10",
      }),
    });

    if (!response.ok) {
      const errText = await response.text();
      return NextResponse.json(
        { error: "Django backend error", details: errText },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    console.error("Error in Next.js chat API route:", error);
    return NextResponse.json(
      { error: "Failed to connect to Django backend", message: error.message },
      { status: 500 }
    );
  }
}
