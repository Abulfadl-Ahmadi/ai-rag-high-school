export interface Citation {
  lesson_number: number;
  lesson_title: string;
  page_start: number;
  page_end: number;
  section_title?: string;
  content_excerpt?: string;
  rrf_score?: number;
}

export interface ExamQuestion {
  id: number;
  question_text: string;
  exam_session: string;
  exam_year: number;
  score: number;
  answer_key: {
    ideal_response: string;
    key_phrases: string[];
    grading_criteria: string;
  };
}

export interface Lesson {
  id: number;
  lesson_number: number;
  title: string;
  part: string;
  page_start: number;
  page_end: number;
}
