// API Configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
export const APP_URL = process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000";

// Role-based routes
export const ROLE_ROUTES = {
  student: "/student",
  institution: "/institution",
  admin: "/admin",
  super_admin: "/super-admin",
};

// Public routes (no auth required)
export const PUBLIC_ROUTES = ["/", "/home", "/login", "/register", "/verify"];

// Protected routes (auth required)
export const PROTECTED_ROUTES = [
  "/student",
  "/institution",
  "/admin",
  "/super-admin",
];

// Auth endpoints
export const AUTH_ENDPOINTS = {
  register_student: "/auth/register/student",
  register_institution: "/auth/register/institution",
  login: "/auth/login",
  refresh: "/auth/refresh",
  logout: "/auth/logout",
};

// Setup endpoints (admin)
export const SETUP_ENDPOINTS = {
  exam_sessions: "/exam-sessions",
  subjects: "/subjects",
  grade_levels: "/grade-levels",
  exam_fees: "/exam-fees",
  exam_centres: "/exam-centres",
};

// Application endpoints
export const APPLICATION_ENDPOINTS = {
  list_user: "/applications/my",
  create: "/applications",
  get: "/applications/[id]",
  update: "/applications/[id]",
  submit: "/applications/[id]/submit",
  list_admin: "/applications/admin",
  approve: "/applications/admin/[id]/approve",
  reject: "/applications/admin/[id]/reject",
};

// Payment endpoints
export const PAYMENT_ENDPOINTS = {
  create_order: "/payments/create-order",
  verify: "/payments/verify",
  webhook: "/payments/webhook",
  list_user: "/payments/my",
  get: "/payments/[id]",
  receipt: "/payments/[id]/receipt",
  list_admin: "/payments/admin",
  admin_get: "/payments/admin/[id]",
};

// Toast messages
export const TOAST_MESSAGES = {
  success: "Operation completed successfully",
  error: "An error occurred. Please try again",
  loading: "Loading...",
  auth_required: "Please log in to continue",
  unauthorized: "You don't have permission to perform this action",
  network_error: "Network error. Please check your connection",
  invalid_credentials: "Invalid email or password",
  registration_success: "Account created successfully. Please log in.",
  application_submitted: "Application submitted successfully",
  payment_success: "Payment verified successfully",
  payment_failed: "Payment verification failed. Please try again",
};

// Pagination defaults
export const PAGINATION = {
  default_page_size: 20,
  max_page_size: 100,
};

// Form validation rules
export const VALIDATION = {
  email_pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  phone_pattern: /^[+]?[(]?[0-9]{1,4}[)]?[-\s.]?[(]?[0-9]{1,4}[)]?[-\s.]?[0-9]{1,9}$/,
  password_min_length: 8,
  pincode_pattern: /^[0-9]{6}$/,
};

// Status colors and labels
export const STATUS_CONFIG = {
  application: {
    draft: { label: "Draft", color: "bg-gray-500", badge: "slate" },
    submitted: {
      label: "Submitted",
      color: "bg-blue-500",
      badge: "blue",
    },
    verification_pending: {
      label: "Under Review",
      color: "bg-amber-500",
      badge: "amber",
    },
    approved: {
      label: "Approved",
      color: "bg-green-500",
      badge: "green",
    },
    payment_pending: {
      label: "Payment Pending",
      color: "bg-indigo-500",
      badge: "indigo",
    },
    paid: { label: "Paid", color: "bg-green-500", badge: "green" },
    rejected: { label: "Rejected", color: "bg-red-500", badge: "red" },
  },
  payment: {
    initiated: { label: "Initiated", color: "bg-blue-500", badge: "blue" },
    pending: { label: "Pending", color: "bg-amber-500", badge: "amber" },
    success: { label: "Success", color: "bg-green-500", badge: "green" },
    failed: { label: "Failed", color: "bg-red-500", badge: "red" },
    refunded: { label: "Refunded", color: "bg-gray-500", badge: "slate" },
  },
};

// Sidebar menu configuration
export const SIDEBAR_MENUS = {
  student: [
    { label: "Dashboard", icon: "LayoutDashboard", href: "/student" },
    {
      label: "Applications",
      icon: "FileText",
      href: "/student/applications",
    },
    {
      label: "New Application",
      icon: "Plus",
      href: "/student/applications/new",
    },
    { label: "Payments", icon: "CreditCard", href: "/student/payments" },
    {
      label: "Admit Cards",
      icon: "Ticket",
      href: "/student/admit-cards",
    },
    { label: "Results", icon: "BarChart3", href: "/student/results" },
    {
      label: "Certificates",
      icon: "Award",
      href: "/student/certificates",
    },
  ],
  institution: [
    { label: "Dashboard", icon: "LayoutDashboard", href: "/institution" },
    {
      label: "Students",
      icon: "Users",
      href: "/institution/students",
    },
    {
      label: "Applications",
      icon: "FileText",
      href: "/institution/applications",
    },
    {
      label: "Payments",
      icon: "CreditCard",
      href: "/institution/payments",
    },
    { label: "Reports", icon: "BarChart3", href: "/institution/reports" },
  ],
  admin: [
    { label: "Dashboard", icon: "LayoutDashboard", href: "/admin" },
    {
      label: "Verification Queue",
      icon: "CheckCircle2",
      href: "/admin/verification",
    },
    {
      label: "Applications",
      icon: "FileText",
      href: "/admin/applications",
    },
    { label: "Payments", icon: "CreditCard", href: "/admin/payments" },
    { label: "Exam Setup", icon: "Settings", submenu: true },
    { label: "Results", icon: "BarChart3", href: "/admin/results" },
    {
      label: "AI Tools",
      icon: "Sparkles",
      href: "/admin/ai-tools",
    },
    { label: "Reports", icon: "FileBarChart", href: "/admin/reports" },
  ],
};
