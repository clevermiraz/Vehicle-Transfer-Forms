export type FatherOrHusband = "father" | "husband";

export interface Person {
  id: number | null;
  name: string;
  father_name: string | null;
  mother_name: string | null;
  spouse_name: string | null;
  father_or_husband_pref: FatherOrHusband;
  guardian_name: string | null;
  gender: "MALE" | "FEMALE" | "OTHER" | null;
  date_of_birth: string | null;
  nationality: string | null;
  nid: string | null;
  tin: string | null;
  phone: string | null;
  present_address: string | null;
  permanent_address: string | null;
}

export interface Vehicle {
  id: number | null;
  registration_number: string;
  vehicle_type: string | null;
  chassis_number: string | null;
  engine_number: string | null;
  manufacturer: string | null;
  manufacturing_year: number | null;
  previous_registration_number: string | null;
}

export interface Witness {
  position?: number;
  name: string;
  address: string | null;
  phone: string | null;
}

export interface Transfer {
  id: number;
  seller: Person;
  buyer: Person;
  vehicle: Vehicle;
  witnesses: Witness[];
  registration_authority: string | null;
  sale_price: number | null;
  sale_price_words: string | null;
  sale_date: string;
  fee_bank_name: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
  created_by: string | null;
  updated_by: string | null;
}

export interface TransferListItem {
  id: number;
  registration_number: string;
  seller_name: string;
  buyer_name: string;
  sale_date: string;
  created_at: string;
}

export interface DocumentInfo {
  slug: string;
  title: string;
  error: string | null;
}

export interface User {
  id: number;
  name: string;
  username: string;
  is_admin: boolean;
  is_active: boolean;
}
