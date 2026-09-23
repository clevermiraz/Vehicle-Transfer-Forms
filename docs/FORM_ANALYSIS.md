# Form Analysis — Vehicle Ownership Transfer

Status: **Draft for review** (Phase 1). No application code has been written yet.
Source files: `reference_forms/` (treated as immutable templates).

---

## 1. Files found

| File | Pages | Size | Producer | Fonts in file | Fillable fields |
|---|---|---|---|---|---|
| `form_20.pdf` | 2 (**page 2 is blank**) | A4 595.44×841.68 pt | MS Word 2016 | NikoshBAN (Unicode), SutonnyMJ Bold (legacy Bijoy) | none |
| `form_21.pdf` | 1 | A4 | MS Word 2019 | NikoshBAN | none |
| `form_22.pdf` | 1 | A4 | MS Word 2019 | NikoshBAN, SutonnyMJ Bold | none |
| `owner_particulars.pdf` | 1 | A4 | MS Word 2016 (Author: "BRTA HQ") | Times New Roman (full embed → 780 KB), NikoshBAN, Nirmala UI | AcroForm present but **empty** (`/Fields: []`) |
| `demo.jpeg` | — | — | — | — | A hand-made mock-up of a filled Form 22 showing the expected output style |

Takeaways:
- None of the PDFs has usable form fields, so every form has to be filled by **drawing text at coordinates** on top of the original page.
- All four are Word exports on A4 with a 72 pt (1 inch) left margin. The dotted rows in Forms 20/21/22 are **24.5 pt apart**.
- Text extraction of the Bangla labels comes out **garbled** (Word wrote broken ToUnicode maps, e.g. `জাতীয়` extracts as `িোতীয়`). We can't find fields by searching for Bangla label text. Instead, coordinates come from the positions of the dotted-leader characters (`.`), which extract exactly. See Appendix A.
- `demo.jpeg` shows the shop's current practice: values are typed in **English, mostly upper-case**, on the dotted lines, and the sale price is written as `5,00,000/- (Five Lac)` on the `এর নিকট` line.

---

## 2. Form summaries

### Form 20 — ফরম-২০: মোটরযানের মালিকানা বদলি সংক্রান্ত বিক্রেতার ঘোষণাপত্র
**Seller's declaration for ownership transfer** (বিধি ৪১(১)).
The seller states: "I, [seller], … declare that the vehicle [reg/type/chassis/engine/maker/year] has been sold to [buyer] … and request transfer of ownership in favour of [buyer], specimen signatures (1)…(2)…".
Signed by the seller (হস্তান্তরকারীর (বিক্রেতা) স্বাক্ষর).

### Form 21 — ফরম-২১: মোটরযানের মালিকানা বদলি সংক্রান্ত ক্রেতার ঘোষণাপত্র
**Buyer's declaration for ownership transfer** (বিধি ৪১(১)).
The buyer states: "I, [buyer], … have bought the vehicle […] from [seller] … and request registration in my name; I attach the registration certificate, fitness certificate, tax token, and route permit (if applicable)."
Signed by the buyer (গ্রহীতার (ক্রেতা) স্বাক্ষর) and, where applicable, the hire-purchase/lien owner (ভাড়া খরিদ/দায়বদ্ধ মালিকের স্বাক্ষর).

### Form 22 — ফরম-২২: বিক্রয় রসিদ
**Sale receipt** (বিধি ৪১(১)(ক)).
The seller states: "I, [seller], … have sold the vehicle […] to [buyer] for [amount] Taka in front of the witnesses below, and have received the full amount."
Has a seller signature, a **revenue stamp box**, and **3 witness slots** (signature, name, address, mobile).

### Owner's Particulars / Specimen Signature — মালিকের ব্যক্তিগত তথ্যাবলি / নমুনা স্বাক্ষর
**BRTA form "For Vehicle Registration or Ownership Transfer".** In a transfer, this is filled for the **new owner (buyer)**.
It has 19 numbered rows (bilingual English/Bangla labels), a **colour photo box** ("3 copies colour photo"), and **4 specimen-signature boxes**.
A footnote says that government, semi-government, or autonomous bodies without an NID/TIN must provide the NID of an authorised person.

---

## 3. Every field, per form

Legend: **R** = rows available (dotted lines), **W** = usable width in pt (approx.), ✍ = manual only.

### Form 20 (page 1 only)
| # | Label (Bangla) | Meaning | Canonical field | R / W |
|---|---|---|---|---|
| 1 | রেজিস্ট্রেশন কর্তৃপক্ষ | Registration authority | `transfer.registration_authority` | 1 / 356 |
| 2 | আমি/আমরা | I/We (seller) | `seller.name` | 1 / 394 |
| 3 | জাতীয় পরিচয়পত্র নম্বর | NID | `seller.nid` | 1 / 125 |
| 4 | টিআইএন নম্বর | TIN | `seller.tin` | 1 / 152 |
| 5 | মাতা | Mother | `seller.mother_name` | 1 / 425 |
| 6 | পিতা/স্বামী | Father/Husband | `seller.father_or_husband` | 1 / 401 |
| 7 | ঠিকানা | Address | `seller.address` | **2** (first row indented) |
| 8 | রেজিস্ট্রেশন নম্বর | Registration no. | `vehicle.registration_number` | 1 / 228 |
| 9 | ধরন | Type | `vehicle.vehicle_type` | 1 / 117 |
| 10 | চেসিস নম্বর | Chassis no. | `vehicle.chassis_number` | 1 / 138 |
| 11 | ইঞ্জিন নম্বর | Engine no. | `vehicle.engine_number` | 1 / 194 |
| 12 | প্রস্তুতকারক | Manufacturer | `vehicle.manufacturer` | 1 / 145 |
| 13 | প্রস্তুতকাল | Year of manufacture | `vehicle.manufacturing_year` | 1 / 190 |
| 14 | জনাব | To Mr./Ms. (buyer) | `buyer.name` | 1 / 418 |
| 15 | পিতা/স্বামী | Buyer's father/husband | `buyer.father_or_husband` | 1 / 398 |
| 16 | ঠিকানা | Buyer's address | `buyer.address` | **2** |
| 17 | মোটরযানটি জনাব | Transfer in favour of (buyer) | `buyer.name` (repeat) | 1 / 366 |
| 18 | নমুনা স্বাক্ষর (১) (২) | Specimen signatures of the transferee | ✍ blank | — |
| 19 | তারিখ | Date | `transfer.document_date` (see Q5) | no dotted line; free space after the label |
| 20 | হস্তান্তরকারীর (বিক্রেতা) স্বাক্ষর | Seller signature | ✍ blank | — |

### Form 21
| # | Label | Meaning | Canonical field | R / W |
|---|---|---|---|---|
| 1 | রেজিস্ট্রেশন কর্তৃপক্ষ | Registration authority | `transfer.registration_authority` | 1 / 359 |
| 2 | আমি/আমরা | I/We (**buyer**) | `buyer.name` | 1 / 394 |
| 3 | জাতীয় পরিচয়পত্র নম্বর | NID | `buyer.nid` | 1 / 124 |
| 4 | টিআইএন নম্বর | TIN | `buyer.tin` | 1 / 156 |
| 5 | মাতা | Mother | `buyer.mother_name` | 1 / 425 |
| 6 | পিতা/স্বামী | Father/Husband | `buyer.father_or_husband` | 1 / 401 |
| 7 | ঠিকানা | Address | `buyer.address` | **1 only** / 418 |
| 8–13 | Reg no. / type / chassis / engine / manufacturer / year | — | `vehicle.*` | 1 each |
| 14 | জনাব | From Mr./Ms. (**seller**) | `seller.name` | 1 / 418 |
| 15 | পিতা/স্বামী | Seller's father/husband | `seller.father_or_husband` | 1 / 398 |
| 16 | ঠিকানা | Seller's address | `seller.address` | **2** |
| 17 | (dotted segment before "উপরে বর্ণিত মোটরযানটির…") | **Unclear** (see Q7) | — | 1 / 214 |
| 18 | তারিখ | Date | `transfer.document_date` | free space |
| 19 | গ্রহীতার (ক্রেতা) স্বাক্ষর | Buyer signature | ✍ | — |
| 20 | ভাড়া খরিদ/দায়বদ্ধ মালিকের স্বাক্ষর | Hire-purchase/lien owner signature | ✍ | — |

### Form 22
| # | Label | Meaning | Canonical field | R / W |
|---|---|---|---|---|
| 1 | আমি/আমরা | I/We (seller) | `seller.name` | 1 / 394 |
| 2 | জাতীয় পরিচয়পত্র নম্বর | NID | `seller.nid` | 1 / 121 |
| 3 | টিআইএন নম্বর | TIN | `seller.tin` | 1 / 153 |
| 4 | মাতা | Mother | `seller.mother_name` | 1 / 425 |
| 5 | পিতা/স্বামী | Father/Husband | `seller.father_or_husband` | 1 / 401 |
| 6 | ঠিকানা | Address | `seller.address` | **3** |
| 7–12 | Reg no. / type / chassis / engine / manufacturer / year | — | `vehicle.*` | 1 each |
| 13 | জনাব | To (buyer) | `buyer.name` | 1 / 418 |
| 14 | পিতা/স্বামী | Buyer's father/husband | `buyer.father_or_husband` | 1 / 398 |
| 15 | ঠিকানা | Buyer's address | `buyer.address` | **2** |
| 16 | এর নিকট …… | Price (the demo writes `5,00,000/- (Five Lac)` here) | `transfer.sale_price` + `transfer.sale_price_words` | 1 / 404 |
| 17 | …… টাকা মূল্যে | Dotted segment right before "Taka" | overflow of price-in-words, or blank (Q8) | 1 / 159 |
| 18 | তারিখ | Date | `transfer.sale_date` | free space |
| 19 | বিক্রেতার স্বাক্ষর | Seller signature | ✍ | — |
| 20 | স্বাক্ষীর স্বাক্ষর, নাম, ঠিকানা ও মোবাইল নম্বর ১।২।৩। | Witnesses 1–3 | `witnesses[i].name/address/phone` (signature ✍) | ~37 pt tall slot each |
| 21 | রেভিনিউ স্ট্যাম্প | Revenue stamp box (x 395–457, y 647–705) | ✍ physical stamp | — |

### Owner's Particulars (values go after the colon at x≈320; usable up to x≈526)
| # | Label | Canonical field (for the **buyer**) | Notes |
|---|---|---|---|
| 1 | NAME (CAPITAL LETTER) | `buyer.name` | Printed in **upper case**. Keep the row to x ≤ 455 so it stays clear of the photo box. |
| 2 | FATHER'S NAME | `buyer.father_name` | **Separate** from husband here |
| 3 | MOTHER'S NAME | `buyer.mother_name` | |
| 4 | HUSBAND/WIFE NAME | `buyer.spouse_name` | optional |
| 5 | PRESENT ADDRESS | `buyer.present_address` | ~2–3 lines at 9–10 pt |
| 6 | PERMANENT ADDRESS | `buyer.permanent_address` | ~2 lines |
| 7 | SEX | `buyer.gender` | |
| 8 | CELL PHONE NO | `buyer.phone` | **only form with a phone number** (apart from witnesses) |
| 9 | NATIONALITY | `buyer.nationality` | default "Bangladeshi" |
| 10 | DATE OF BIRTH | `buyer.date_of_birth` | |
| 11 | NID NO. | `buyer.nid` | |
| 12 | e-TIN NO | `buyer.tin` | |
| 13 | GUARDIAN'S NAME (minor) | `buyer.guardian_name` | optional |
| 14 | VEHICLE REGISTRATION NO | `vehicle.registration_number` | |
| 15 | ENGINE NO | `vehicle.engine_number` | |
| 16 | CHASSIS NO | `vehicle.chassis_number` | |
| 17 | YEAR OF MFG | `vehicle.manufacturing_year` | |
| 18 | PREV. REGISTRATION NO (if any) | `vehicle.previous_registration_number` | optional (reconditioned/special registration) |
| 19 | BANK NAME for Fee/Tax deposit | `transfer.fee_bank_name` | ⚠ the bank where BRTA fees are paid. **Not** a loan/lien bank. |
| — | Photo box (x 458–533, y 73–144) | — | ✍ physical photo (see §11) |
| — | Specimen signature 1–4 | — | ✍ |

---

## 4. Common fields (field → forms)

| Canonical field | F20 | F21 | F22 | OP |
|---|:-:|:-:|:-:|:-:|
| `vehicle.registration_number` | ✔ | ✔ | ✔ | ✔ |
| `vehicle.engine_number` | ✔ | ✔ | ✔ | ✔ |
| `vehicle.chassis_number` | ✔ | ✔ | ✔ | ✔ |
| `vehicle.manufacturing_year` | ✔ | ✔ | ✔ | ✔ |
| `vehicle.vehicle_type` | ✔ | ✔ | ✔ | |
| `vehicle.manufacturer` | ✔ | ✔ | ✔ | |
| `seller.name` | ✔ | ✔ | ✔ | |
| `seller.father_or_husband` | ✔ | ✔ | ✔ | |
| `seller.address` | ✔ (2 rows) | ✔ (2) | ✔ (3) | |
| `seller.nid`, `seller.tin`, `seller.mother_name` | ✔ | | ✔ | |
| `buyer.name` | ✔ (×2) | ✔ | ✔ | ✔ |
| `buyer.father_or_husband` | ✔ | ✔ | ✔ | (split into father + spouse) |
| `buyer.address` | ✔ (2) | ✔ (1) | ✔ (2) | present + permanent |
| `buyer.nid`, `buyer.tin`, `buyer.mother_name` | | ✔ | | ✔ |
| `transfer.registration_authority` | ✔ | ✔ | | |
| date | ✔ | ✔ | ✔ | |

The vehicle block is identical in Forms 20, 21, and 22 (same six fields, same layout).

## 5. Fields that appear in only one form
- **Form 20:** "মোটরযানটি জনাব" (buyer name again, as transferee); specimen signatures (১)(২) — manual.
- **Form 21:** unclear dotted segment (Q7); hire-purchase/lien owner signature — manual.
- **Form 22:** sale price (figures + words); witnesses 1–3; revenue stamp.
- **Owner Particulars:** gender, phone, nationality, date of birth, guardian, present vs permanent address, previous registration no., fee bank name, photo, 4 specimen signatures.

## 6. Field groups
- **Seller:** name, father_name, spouse_name → father_or_husband, mother_name, nid, tin, address (single "ঠিকানা").
- **Buyer:** everything above plus phone, gender, nationality, date_of_birth, guardian_name, present_address, permanent_address.
- **Vehicle:** registration_number, vehicle_type, chassis_number, engine_number, manufacturer, manufacturing_year, previous_registration_number.
- **Transaction:** registration_authority, sale_price, sale_price_words, sale_date, document_date, fee_bank_name.
- **Witness (Form 22):** name, address, phone (×3).
- **General:** form title/rule text (already printed).
- **Other / manual:** signatures, revenue stamp, photo.

## 7. Canonical field mapping table

| Canonical field | Form 20 | Form 21 | Form 22 | Owner Particulars |
|---|---|---|---|---|
| `seller.name` | আমি/আমরা | জনাব | আমি/আমরা | — |
| `seller.nid` | জাতীয় পরিচয়পত্র নম্বর | — | জাতীয় পরিচয়পত্র নম্বর | — |
| `seller.tin` | টিআইএন নম্বর | — | টিআইএন নম্বর | — |
| `seller.mother_name` | মাতা | — | মাতা | — |
| `seller.father_or_husband` | পিতা/স্বামী | পিতা/স্বামী (2nd block) | পিতা/স্বামী | — |
| `seller.address` | ঠিকানা (2 rows) | ঠিকানা (2nd block, 2 rows) | ঠিকানা (3 rows) | — |
| `buyer.name` | জনাব; মোটরযানটি জনাব | আমি/আমরা | জনাব | 1 NAME (upper-case) |
| `buyer.nid` | — | জাতীয় পরিচয়পত্র নম্বর | — | 11 NID NO. |
| `buyer.tin` | — | টিআইএন নম্বর | — | 12 e-TIN NO |
| `buyer.mother_name` | — | মাতা | — | 3 MOTHER'S NAME |
| `buyer.father_name` | via father_or_husband | via father_or_husband | via father_or_husband | 2 FATHER'S NAME |
| `buyer.spouse_name` | via father_or_husband | via father_or_husband | via father_or_husband | 4 HUSBAND/WIFE NAME |
| `buyer.present_address` | ঠিকানা (2 rows) | ঠিকানা (1 row) | ঠিকানা (2 rows) | 5 PRESENT ADDRESS |
| `buyer.permanent_address` | — | — | — | 6 PERMANENT ADDRESS |
| `buyer.gender / phone / nationality / date_of_birth / guardian_name` | — | — | — | 7 / 8 / 9 / 10 / 13 |
| `vehicle.registration_number` | রেজিস্ট্রেশন নম্বর | রেজিস্ট্রেশন নম্বর | রেজিস্ট্রেশন নম্বর | 14 |
| `vehicle.vehicle_type` | ধরন | ধরন | ধরন | — |
| `vehicle.chassis_number` | চেসিস নম্বর | চেসিস নম্বর | চেসিস নম্বর | 16 |
| `vehicle.engine_number` | ইঞ্জিন নম্বর | ইঞ্জিন নম্বর | ইঞ্জিন নম্বর | 15 |
| `vehicle.manufacturer` | প্রস্তুতকারক | প্রস্তুতকারক | প্রস্তুতকারক | — |
| `vehicle.manufacturing_year` | প্রস্তুতকাল | প্রস্তুতকাল | প্রস্তুতকাল | 17 YEAR OF MFG |
| `vehicle.previous_registration_number` | — | — | — | 18 |
| `transfer.registration_authority` | রেজিস্ট্রেশন কর্তৃপক্ষ | রেজিস্ট্রেশন কর্তৃপক্ষ | — | — |
| `transfer.sale_price` (+ words) | — | — | এর নিকট … টাকা মূল্যে | — |
| `transfer.sale_date` | — | — | তারিখ | — |
| `transfer.document_date` | তারিখ | তারিখ | — | — |
| `transfer.fee_bank_name` | — | — | — | 19 BANK NAME |
| `witnesses[0..2].name/address/phone` | — | — | ১। ২। ৩। | — |

Derived value: `father_or_husband` = father's name by default, or husband's name if the person has chosen that (see §8, Q3).

## 8. Same meaning, different labels
- **"আমি/আমরা"** is the seller in Forms 20 and 22 but the **buyer** in Form 21.
- **"জনাব"** is the buyer in Forms 20 and 22 but the **seller** in Form 21.
- **"পিতা/স্বামী"** (father *or* husband: one slot) in Forms 20/21/22 corresponds to the separate "FATHER'S NAME" and "HUSBAND/WIFE NAME" rows in OP. We store both and derive the combined slot.
- **"ঠিকানা"** (single address) in Forms 20/21/22 corresponds to "PRESENT ADDRESS" + "PERMANENT ADDRESS" in OP. We use the present address for the single slot unless the owner decides otherwise (Q4).
- **"প্রস্তুতকাল"** (time of manufacture) = "YEAR OF MFG" = `manufacturing_year`.
- **"TIN" (Forms 20–22)** = **"e-TIN" (OP)**.
- **"ধরন"** = vehicle type/class (e.g. `CAR (HATCH BACK)`, `MOTOR CYCLE`).

## 9. Optional fields
TIN (not everyone has an e-TIN), spouse name, guardian name (minors only), previous registration no. (reconditioned/special only), witnesses (Form 22 has 3 slots; how many are required is Q9), phone for sellers (no form uses it, but it helps search), fee bank name (may not be known at data-entry time).

## 10. Signature / manual-only areas — keep blank
| Form | Area |
|---|---|
| F20 | নমুনা স্বাক্ষর (১) (২); হস্তান্তরকারীর (বিক্রেতা) স্বাক্ষর |
| F21 | গ্রহীতার (ক্রেতা) স্বাক্ষর; ভাড়া খরিদ/দায়বদ্ধ মালিকের স্বাক্ষর |
| F22 | বিক্রেতার স্বাক্ষর; witness signatures; রেভিনিউ স্ট্যাম্প box |
| OP | Specimen signature boxes 1–4; photo box |

The MVP draws nothing in these areas.

## 11. Image / photo fields
Only OP has one: "৩ কপি রঙিন ছবি / 3 copies colour photo", a box at x 458–533, y 73–144 (≈26×25 mm).
**Recommendation: Option A — leave it blank for a physical photo.** The form asks for 3 physical copies, so the customer brings prints anyway. Uploading photos would add image storage, cropping UI, and more personal-data handling for no real gain. We can add it later if the owner wants it.

## 12. Fields that must stay blank for manual completion
All items in §10, plus any field the operator leaves empty. Empty values print nothing, so the original dotted line stays visible for handwriting.

## 13. Bangla requirements
- Every template label is Bangla (except the English labels in OP). **Our overlay text can be English, Bangla, or mixed.**
- The demo uses English upper-case values. OP asks for "NAME (CAPITAL LETTER)", i.e. English.
- Addresses and names may still be typed in Bangla (NID cards carry both), so Bangla rendering must be correct.
- Numbers: the forms mix Bangla and ASCII digits. Values like the registration number (`ঢাকা মেট্রো-গ-১২-৩৪৫৬` vs `DHAKA METRO-GA-12-3456`) could come in either script (Q2).

## 14. PDF rendering / font findings (tested with PyMuPDF 1.28.2)

| Test | Result |
|---|---|
| `page.insert_text()` with a Bengali TTF | ❌ **Broken Bangla.** It does no complex-script shaping: `মোঃ` → `মেোঃ`, conjuncts (`শ্রী`, `ক্ষ`, `ঞ্জ`, `স্ত্র`) break into hasanta forms, and Latin letters show as tofu boxes if the font has no Latin glyphs. **Must not be used for Bangla.** |
| `page.insert_htmlbox()` (MuPDF Story engine with HarfBuzz) | ✅ Correct shaping of every conjunct tested (`শ্রীকৃষ্ণ`, `দক্ষিণ`, `হবিগঞ্জ`, `স্ত্রী`, `বাড়ি`) and of mixed Bangla/English in one run. |
| Font fallback chain in CSS (`font-family: latin, bengali`) | ✅ English goes to Noto Sans and Bangla to Noto Sans Bengali, automatically. |
| Multi-line wrapping with `line-height: 24.5pt` | ✅ Wrapped lines sit exactly on the form's dotted rows. |
| Built-in `scale_low` shrink-to-fit | ⚠ It shrinks the **whole box, line spacing included**, so the text drifts off the dotted rows. We need our own loop that shrinks only the font size and keeps the row pitch. |

Other issues:
- **SutonnyMJ (legacy Bijoy/ANSI encoding)** in the templates is only used in the static title text we never touch. We must *not* use SutonnyMJ/Bijoy fonts for values, because they need non-Unicode input. All data stays Unicode.
- **Font choice:** Noto Sans Bengali and Noto Sans (SIL OFL, free to bundle) both work. To match the template's look, *Nikosh* (the Bangladesh government's Unicode font) is an alternative, but its redistribution licence should be confirmed first (Q10). The subsets embedded in the templates can't be reused.
- **Page 2 of Form 20 is blank.** Output should contain page 1 only.
- **File size:** OP embeds full Times New Roman (780 KB). Output will be similar; we will call `subset_fonts()` and save with `garbage=3, deflate=True`.
- **Garbled text extraction** in the templates (Bangla labels) doesn't affect rendering, only coordinate discovery (see Appendix A).
- **Row start positions:** a multi-row field's first row starts after its label (e.g. x=105) and the continuation rows start at x=72. Plan: one box spanning all rows from x=72 with CSS `text-indent` for the first row. This needs checking in Step 5; the fallback is one box per row with our own line breaking.

## 15. Recommended PDF generation approach

**PyMuPDF only. Overlay on the untouched original template using `insert_htmlbox`, with bundled Unicode fonts.**

```
generate_pdf(template_path, mapping, data) -> bytes
  doc = pymupdf.open(template_path)          # original file is never written
  drop pages not listed in mapping           # e.g. Form 20 page 2
  for field in mapping.fields:
      text = resolve(data, field.key)        # "seller.address" → value (+ optional transform)
      if not text: continue                  # blank → dotted line stays for handwriting
      fit_text(page, field.box, text, field.font_size, field.min_font_size, field.row_pitch)
  doc.subset_fonts(); return doc.tobytes(garbage=3, deflate=True)
```

- **fit_text:** start at the configured size (≈11 pt on the 14 pt forms, 9–10 pt on OP) and step down to `min_font_size` (≈7.5 pt), keeping line-height = row pitch. If the text still doesn't fit, **raise `FieldOverflowError(form, field)`**. The API returns it and the UI shows "Seller address is too long for Form 22 — please shorten". It never clips silently.
- **Mapping** = one plain Python module per form (`mappings/form22.py`) containing a list of `FieldBox(key, page, x0, x1, first_baseline, rows, first_row_indent, font_size, transform)`. The coordinates come from Appendix A.
- **Transforms** (small, explicit): `upper`, `date_dmy`, `money_bd` (`5,00,000/-`), `money_words`, `bn_digits` (if needed).
- **Why not the alternatives:** ReportLab has no Bangla shaping by default. WeasyPrint shapes correctly, but we would have to redraw the whole form in HTML, which fights the requirement to look like the original. pypdf can't shape text. PyMuPDF does everything we need in one dependency.
- **Visual regression test:** render the output at 150 dpi and compare it with a stored "golden" PNG in the tests, plus automated checks that no field overflowed.

## 16. Proposed data model (improved from the suggested one)

Two changes from the brief, and why:
1. **Joint owners.** The forms say "আমি/**আমরা**" (I/**we**), and F20/OP have multiple specimen-signature slots. So a transfer can have more than one seller or buyer. Instead of `seller_id`/`buyer_id` columns, use a `transfer_parties` table with `role` + `position`. The MVP UI shows one seller and one buyer, and the schema doesn't block more later (Q1).
2. **Snapshots.** A printed transfer must re-print exactly the same, even if the person later changes address. `Person` and `Vehicle` are **reusable master records for auto-fill**. The transfer keeps a **copy** of the values used at save time in `transfer_parties` and in vehicle columns on the transfer. It duplicates some data on purpose, for legal-document correctness, and it also makes search simple (one join, indexed columns).

```
users            id, name, username (unique), password_hash, is_active, is_admin, created_at

people           id, name, name_bn?, father_name, mother_name, spouse_name,
                 father_or_husband_pref ('father'|'husband', default 'father'),
                 guardian_name, gender, date_of_birth, nationality='Bangladeshi',
                 nid (unique, nullable), tin, phone, present_address, permanent_address,
                 created_at/by, updated_at/by

vehicles         id, registration_number, registration_number_norm (unique, for search),
                 vehicle_type, chassis_number (unique), engine_number, manufacturer,
                 manufacturing_year, previous_registration_number, timestamps

ownership_transfers
                 id, vehicle_id → vehicles,
                 -- vehicle snapshot:
                 registration_number, registration_number_norm, vehicle_type, chassis_number,
                 engine_number, manufacturer, manufacturing_year, previous_registration_number,
                 registration_authority, sale_price (integer taka), sale_price_words,
                 sale_date, document_date, fee_bank_name, notes,
                 created_at/by, updated_at/by

transfer_parties id, transfer_id, person_id → people (nullable), role ('seller'|'buyer'),
                 position (1..n), + snapshot of all person fields above

witnesses        id, transfer_id, position (1..3), name, address, phone
```

**Save flow (one DB transaction):** upsert `people` (matched by NID) and `vehicles` (matched by normalised reg no. / chassis no.), then write the transfer, its snapshots, and the witnesses.

**Validation:**
- NID: 10, 13, or 17 digits.
- e-TIN: 12 digits.
- Mobile: `01[3-9]` + 8 digits (`+880`/`880` prefix accepted and normalised).
- Year: 1950 … current year + 1.
- Price: a positive integer.
- Bangla digits in input are converted to ASCII before validating and searching.

## 17. Proposed folder structure

```
Form Refill/
  reference_forms/            # originals — read-only
  docs/FORM_ANALYSIS.md
  backend/
    pyproject.toml  alembic.ini  .env.example
    alembic/versions/
    app/
      main.py                 # FastAPI app, CORS, routers
      core/                   # config (env), security (hashing, JWT/cookie), deps
      db/                     # engine, session, Base
      models/                 # user, person, vehicle, ownership_transfer (+party), witness
      schemas/                # pydantic in/out
      api/                    # auth, people, vehicles, transfers, documents
      services/
        transfers.py          # save/upsert logic (DB transaction)
        pdf/
          generator.py        # generate_pdf(), fit_text(), transforms
          fonts/              # NotoSans-Regular.ttf, NotoSansBengali-Regular.ttf (+ OFL)
          mappings/  form20.py form21.py form22.py owner_particulars.py
    tests/                    # validation, save flow, pdf overflow, golden-image tests
  frontend/                   # Next.js + TS + Tailwind
    app/ login/  page.tsx (dashboard+search)  transfers/new/  transfers/[id]/ (review+docs)
```

`reference_forms/` stays at the project root, and the backend reads it through a configured path, so nothing gets copied or modified.

**API** (as in the brief, one addition):
- `GET /api/transfers?q=` searches reg no., NID, mobile, seller name, and buyer name.
- `GET /api/transfers/{id}/documents/{form}?disposition=inline|attachment`
- `GET /api/transfers/{id}/documents/all.zip`
- `GET /api/transfers/{id}/documents/all.pdf`: a single merged PDF for **Print All** (one print dialog), which is trivial with PyMuPDF.

---

## 18. Questions for the shop owner (answers needed before final implementation)

1. **Joint owners:** how often is there more than one seller or buyer? If there are two buyers, do we fill one Owner Particulars sheet **per buyer**, and do both names go on the "আমি/আমরা" line?
2. **Language of values:** always English (as in the demo), always Bangla, or per-customer? Should OP always be English upper case? Should registration numbers be stored as `DHAKA METRO-GA-…` or `ঢাকা মেট্রো-গ-…`?
3. **পিতা/স্বামী:** for a married woman, is the husband's name written, or the father's? (Proposal: store both, choose per person, default father.)
4. **Address in Forms 20/21/22:** present address or permanent address?
5. **Dates:** do F20 and F21 use the sale date, the submission date, or stay blank for handwriting? What format: `23/09/2026`, `২৩/০৯/২০২৬`, or `23-Sep-2026`?
6. **Upper case:** should all English values be printed in upper case, like the demo?
7. **Form 21:** what goes on the dotted segment right before "উপরে বর্ণিত মোটরযানটির মালিকানা…" (the 4th seller-address line, a date, or nothing)?
8. **Form 22 price:** is the demo's `5,00,000/- (Five Lac)` on the "এর নিকট" line the standard format? Should the amount in words be in English or Bangla ("পাঁচ লক্ষ")? Should anything go on the short dotted segment before "টাকা মূল্যে"?
9. **Witnesses:** how many are usually required (1–3)? Should their name/address/phone be printed, or handwritten when they sign? Are the witnesses often the same people (e.g. shop staff), so we should keep a quick-pick list?
10. **Font:** is Noto Sans Bengali acceptable, or should the output match the Nikosh look of the printed labels?
11. **Revenue stamp / photo / signatures:** confirm all stay manual (recommended).
12. **Fee bank (OP #19):** is it usually the same bank (so it can be a default)?
13. **Printer:** A4 on a laser printer? Any known margin offset we should compensate for?
14. **Other forms:** are there more documents in a transfer (e.g. application form, affidavit) to add later?
15. **Users:** how many staff logins? Is a single "admin" role enough for managing users?

---

## 19. Decisions (answered 2026-09-23)

| # | Topic | Decision |
|---|---|---|
| 1 | Joint owners | Always **1 seller + 1 buyer** in the UI. The `transfer_parties` table stays, so joint owners can be added later without a migration. |
| 2 | Language | Values are **English, printed in CAPITAL letters** (Latin text is upper-cased at render time). Bangla is still allowed if typed and must render correctly. No separate `name_bn` fields. |
| 3 | পিতা/স্বামী | Store both father and husband. A **per-person toggle** (`father_or_husband_pref`, default `father`) picks which one prints. OP prints both on their own rows. |
| 4 | Address on F20/21/22 | **Present address.** The permanent address appears only on OP. |
| 5 | Dates on F20/21/22 | **Sale date on all three** (default: today). `document_date` is dropped. |
| 6 | Date format | **DD/MM/YYYY** with English digits (e.g. `20/09/2026`). |
| 7 | Form 21 unclear dotted segment | **Leave blank.** |
| 8 | Form 22 price | `5,00,000/- (Five Lac)`: figures in Bangladeshi grouping + English words, auto-generated and editable. |
| 9 | Witnesses | **Optional, 0–3.** Name, address, and mobile are printed when entered; empty slots stay blank. |
| 10 | Witness quick-pick | **No.** Witnesses are typed each time. |
| 11 | Font | **Noto Sans** (Latin) + **Noto Sans Bengali**, bundled (OFL). |
| 12 | Photo / signatures / revenue stamp | **All blank** (manual). |
| 13 | Fee bank & registration authority | **Pre-filled from the last transfer**, editable. |
| 14 | Printer | **A4, 100% scale**, full form printed on plain paper. A printer offset setting can come later if needed. |
| 15 | Users | **Admin + staff** logins. Admin can add/disable staff. `created_by`/`updated_by` are recorded. |

Not yet asked: whether other documents (application form, affidavit, etc.) will be needed later. This doesn't block the MVP.

---

## Appendix A — Measured coordinates (PDF points, origin top-left)

These are the dotted-leader runs (x-start → x-end) and text baselines, extracted from the character boxes. They are the starting point for the mappings and will be fine-tuned against printed output in Step 5/6.

**Form 20:** reg authority y=149.5 x161–517 · seller name 174.0 x128–522 · NID 198.5 x176–301 / TIN x369–521 · mother 223.1 x97–522 · father/husband 247.6 x121–522 · address 272.1 x105–523 + 296.6 x72–522 · reg no 345.6 x147–375 / type x401–518 · chassis 370.1 x128–266 / engine x323–517 · maker 394.6 x127–272 / year x324–514 · buyer name 443.7 x103–521 · buyer father 468.2 x124–522 · buyer address 492.7 x108–523 + 517.2 x72–522 · "মোটরযানটি জনাব" 541.6 x157–523 · specimen sig 590.7 x85–220 / x238–369 (blank) · date label "তারিখ:" at y≈688, x72–106.

**Form 21:** reg authority 148.2 x164–523 · buyer name 172.7 x128–522 · NID 197.2 x176–300 / TIN x368–524 · mother 221.8 x97–522 · father 246.3 x121–522 · address 270.8 x105–523 · reg no 319.7 x146–378 / type x403–524 · chassis 344.3 x128–273 / engine x326–524 · maker 368.8 x127–275 / year x323–524 · seller name 417.8 x103–521 · seller father 442.4 x124–522 · seller address 466.9 x108–523 + 491.4 x72–522 · unclear segment 515.8 x72–286 · date label at y≈662, x77–111.

**Form 22:** seller name 134.7 x128–522 · NID 159.3 x176–297 / TIN x369–522 · mother 183.7 x97–522 · father 208.2 x121–522 · address 232.7 x105–523 + 257.2 x72–522 + 281.8 x72–522 · reg no 330.8 x150–372 / type x397–518 · chassis 355.2 x128–273 / engine x327–517 · maker 379.9 x127–276 / year x324–518 · buyer name 404.3 x103–521 · buyer father 428.8 x124–522 · buyer address 453.3 x108–523 + 477.9 x72–522 · price ("এর নিকট") 502.4 x117–521 · pre-"টাকা" segment 526.9 x72–231 · date label y≈596, x72–106 · witnesses 1/2/3 label baselines ≈ 662 / 699 / 735, text from x≈92 · revenue stamp box x395–457 y647–705.

**Owner Particulars:** colons at x312–317 for all rows. Values start x≈322. Row tops (label line 1): 1 Name 140.5 · 2 Father 163.7 · 3 Mother 188.1 · 4 Spouse 212.3 · 5 Present addr 236.7 (block to ≈270) · 6 Permanent addr 272.2 (to ≈294) · 7 Sex 296.5 · 8 Phone 320.8 · 9 Nationality 345.1 · 10 DOB 369.4 · 11 NID 393.7 · 12 TIN 418.0 · 13 Guardian 442.9 · 14 Reg no 466.0 · 15 Engine 501.1 · 16 Chassis 527.2 · 17 Year 551.6 · 18 Prev reg 575.9 · 19 Bank 645.3 · photo box x458–533 y73–144.

## Appendix B — Evidence
Render tests are in `/tmp/formrender/` (scratch, not part of the project):
- `f22_test-1.png`: `insert_text` (broken) vs `insert_htmlbox` (correct)
- `f22_test2-1.png`: row-aligned wrapping, and why `scale_low` isn't suitable
