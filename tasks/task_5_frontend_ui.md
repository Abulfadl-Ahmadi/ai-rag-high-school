# Task 5: Interactive Web UI & High School Tutor Experience

## 🎯 Objective
Create a responsive, modern Persian web interface (RTL) tailored for Iranian high school students, integrating live streaming chat, lesson navigation, source inspection modals, and exam intelligence widgets.

## 📁 Allowed Files
- `frontend/index.html` [NEW]
- `frontend/app.js` [NEW]
- `frontend/styles.css` [NEW]
- `backend/knowledge/templates/knowledge/index.html` [NEW]

## 🛠️ Implementation Rules
1. **Design System & Aesthetics**: Clean Iranian educational theme (Emerald/Indigo palette, Vazirmatn typography, high contrast, smooth animations).
2. **Interactive Components**:
   - **Header & Breadcrumbs**: Subject selector, Grade 12 tag, Lesson dropdown (`درس ۱ تا ۱۰`).
   - **Dual Pane Layout**:
     - Left / Main Pane: Chat stream with markdown parsing, Arabic verse callouts (`قَالَ إِنِّي...`), copy buttons, and citation badges `[درس ۶، صفحه ۸۲]`.
     - Right Sidebar: **Source Inspector** (live textbook excerpt with highlight) + **Exam Intelligence Card** (past exam appearances, frequency rating ⭐⭐⭐⭐⭐).
   - **Quick Action Prompts**: `[ ⚡ توضیح ساده‌تر ]`, `[ 📝 نمونه سوال نهایی ]`, `[ 📖 پیام و تدبر در آیات ]`, `[ 🎯 مرور شب امتحان ]`.
3. **Robust Client Logic**: Support both SSE real-time streaming and JSON fallback, lesson filtering, and session persistence.

## 📊 Deliverables
- Working responsive web application connected to the backend.
- Execution report saved to `./tasks/reports/report_task_5.md`.
