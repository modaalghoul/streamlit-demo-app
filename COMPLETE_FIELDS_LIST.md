# قائمة الحقول الكاملة - Complete Fields List

## جميع حقول جدول الأدوية (Medications Table)

### 📌 المعلومات الأساسية / Basic Information
| Field Name | Arabic Name | Type | Required |
|------------|-------------|------|----------|
| id | المعرف | INTEGER | Auto |
| generic_name | الاسم العلمي | VARCHAR(200) | ✅ Yes |
| trade_name | الاسم التجاري | VARCHAR(200) | No |
| category_id | معرف الفئة | INTEGER | No |
| drug_type_id | معرف نوع الدواء | INTEGER | No |
| manufacturer_id | معرف الشركة المصنعة | INTEGER | No |
| concentration | التركيز | VARCHAR(100) | No |
| form | الشكل الصيدلاني | VARCHAR(100) | No |
| active_ingredient | المادة الفعالة | TEXT | No |
| composition | التركيب الكامل | TEXT | No |

### 👶 الحدود العمرية / Age Limits
| Field Name | Arabic Name | Type | Required |
|------------|-------------|------|----------|
| min_age_months | الحد الأدنى للعمر (شهور) | INTEGER | No |
| max_age_months | الحد الأقصى للعمر (شهور) | INTEGER | No |
| age_limit_text | الحد العمري (نص) | VARCHAR(200) | No |

### ⚖️ الحدود الوزنية / Weight Limits
| Field Name | Arabic Name | Type | Required |
|------------|-------------|------|----------|
| min_weight_kg | الحد الأدنى للوزن (كجم) | DECIMAL(5,2) | No |
| max_weight_kg | الحد الأقصى للوزن (كجم) | DECIMAL(5,2) | No |
| weight_limit_text | الحد الوزني (نص) | VARCHAR(200) | No |

### 💊 معلومات الجرعة / Dosage Information
| Field Name | Arabic Name | Type | Required |
|------------|-------------|------|----------|
| max_single_dose | الجرعة القصوى للجرعة الواحدة | VARCHAR(100) | No |
| dose_calculation | معادلة حساب الجرعة | TEXT | No |
| max_daily_dose | الجرعة القصوى اليومية | VARCHAR(100) | No |
| frequency | التكرار | VARCHAR(100) | No |
| duration | المدة | VARCHAR(100) | No |
| administration_route | طريقة الإعطاء | VARCHAR(100) | No |

### ⚕️ المعلومات الطبية / Medical Information
| Field Name | Arabic Name | Type | Required |
|------------|-------------|------|----------|
| indications | دواعي الاستعمال | TEXT | No |
| contraindications | محاذير الاستخدام | TEXT | No |
| side_effects | الآثار الجانبية | TEXT | No |
| drug_interactions | التفاعلات الدوائية | TEXT | No |
| warnings | تحذيرات | TEXT | No |
| precautions | احتياطات | TEXT | No |
| overdose_management | إدارة الجرعة الزائدة | TEXT | No |

### 🤰 الحمل والرضاعة / Pregnancy & Lactation
| Field Name | Arabic Name | Type | Required |
|------------|-------------|------|----------|
| pregnancy_category | فئة الحمل | VARCHAR(10) | No |
| pregnancy_safety | الأمان أثناء الحمل | TEXT | No |
| lactation_safety | الأمان أثناء الرضاعة | TEXT | No |

### 📦 ظروف التخزين / Storage Conditions
| Field Name | Arabic Name | Type | Required |
|------------|-------------|------|----------|
| storage_conditions | ظروف التخزين | TEXT | No |
| shelf_life | مدة الصلاحية | VARCHAR(100) | No |
| storage_after_opening | التخزين بعد الفتح | VARCHAR(100) | No |

### 💰 المعلومات التجارية / Commercial Information
| Field Name | Arabic Name | Type | Required |
|------------|-------------|------|----------|
| warehouse_name | اسم المستودع | VARCHAR(200) | No |
| package_info | التعبئة | VARCHAR(200) | No |
| package_size | حجم العبوة | VARCHAR(100) | No |
| price | السعر | DECIMAL(10,2) | No |
| price_with_tax | السعر مع الضريبة | DECIMAL(10,2) | No |
| availability | التوفر | VARCHAR(50) | No |
| barcode | الباركود | VARCHAR(100) | No |

### 🖼️ الصور والمستندات / Images & Documents
| Field Name | Arabic Name | Type | Required |
|------------|-------------|------|----------|
| image_path | مسار صورة الدواء | VARCHAR(500) | No |
| leaflet_path | مسار النشرة الطبية | VARCHAR(500) | No |
| box_image_path | مسار صورة العلبة | VARCHAR(500) | No |
| additional_images | صور إضافية | TEXT | No |

### 🌍 معلومات المنشأ / Origin Information
| Field Name | Arabic Name | Type | Required |
|------------|-------------|------|----------|
| manufacturing_country | بلد التصنيع | VARCHAR(100) | No |
| marketing_country | بلد التسويق | VARCHAR(100) | No |
| license_number | رقم الترخيص | VARCHAR(100) | No |

### 📝 ملاحظات / Notes
| Field Name | Arabic Name | Type | Required |
|------------|-------------|------|----------|
| notes | ملاحظات عامة | TEXT | No |
| pharmacist_notes | ملاحظات الصيدلي | TEXT | No |

### 📅 التواريخ / Timestamps
| Field Name | Arabic Name | Type | Required |
|------------|-------------|------|----------|
| created_at | تاريخ الإنشاء | TIMESTAMP | Auto |
| updated_at | تاريخ التحديث | TIMESTAMP | Auto |

---

## إجمالي الحقول / Total Fields
- **إجمالي الحقول:** 54 حقل
- **الحقول المطلوبة:** 1 حقل فقط (generic_name)
- **الحقول الاختيارية:** 53 حقل

## ملاحظات / Notes
- جميع الحقول متوفرة الآن في نموذج إضافة الدواء
- جميع الحقول تظهر في صفحة تفاصيل الدواء
- الحقول منظمة في أقسام منطقية لسهولة الاستخدام
- يمكن ترك أي حقل اختياري فارغاً
