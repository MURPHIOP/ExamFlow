export enum ApplicationStatus {
  DRAFT = "draft",
  SUBMITTED = "submitted",
  PAYMENT_PENDING = "payment_pending",
  PAID = "paid",
  UNDER_VERIFICATION = "under_verification",
  APPROVED = "approved",
  REJECTED = "rejected",
  CORRECTION_REQUIRED = "correction_required",
  CENTRE_ALLOCATED = "centre_allocated",
  ADMIT_CARD_GENERATED = "admit_card_generated",
  EXAM_COMPLETED = "exam_completed",
  MARKS_ENTERED = "marks_entered",
  RESULT_PUBLISHED = "result_published",
  CERTIFICATE_ISSUED = "certificate_issued",
  CERTIFICATE_REVOKED = "certificate_revoked",
}

export enum PaymentStatus {
  PENDING = "pending",
  PAID = "paid",
  FAILED = "failed",
  REFUNDED = "refunded",
}

export enum DocumentStatus {
  NOT_GENERATED = "not_generated",
  GENERATED = "generated",
  REGENERATED = "regenerated",
  REVOKED = "revoked",
}

export enum ExamArtForm {
  MUSIC = "music",
  DANCE = "dance",
  DRAWING = "drawing",
  PAINTING = "painting",
  KARATE = "karate",
  TABLA = "tabla",
  VOCAL = "vocal",
  INSTRUMENTAL = "instrumental",
  RABINDRA_SANGEET = "rabindra_sangeet",
  CLASSICAL_DANCE = "classical_dance",
  FINE_ARTS = "fine_arts",
  OTHERS = "others",
}

export enum ThemeMode {
  LIGHT = "light",
  DARK = "dark",
  SYSTEM = "system",
}
