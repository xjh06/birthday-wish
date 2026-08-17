export interface BirthdayInfo {
  recipientName: string;
  birthdayDate: string;
  heroTitle: string;
  blessingTitle: string;
  blessingText: string;
  cardSalutation: string;
  cardMessage: string;
  musicUrl: string;
}

export interface BirthdayMessage {
  id: number | string;
  senderName: string;
  relationship: string;
  content: string;
  likeCount: number;
  createdAt: string;
  visible: boolean;
}

export interface CreateMessagePayload {
  senderName: string;
  relationship: string;
  content: string;
}

export interface BirthdayStats {
  visitCount: number;
  messageCount: number;
  totalLikes: number;
}

export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

export interface PageResult<T> {
  content: T[];
  page: number;
  size: number;
  totalElements: number;
  totalPages: number;
}
