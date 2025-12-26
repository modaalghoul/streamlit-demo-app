-- ===================================================================
-- قاعدة بيانات نظام إدارة الأدوية
-- Drug Management System Database Schema
-- ===================================================================

-- تفعيل Foreign Keys في SQLite
PRAGMA foreign_keys = ON;

-- ===================================================================
-- 1. جدول الفئات الرئيسية (Categories)
-- ===================================================================
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    name_ar VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- إضافة بيانات أولية للفئات
INSERT INTO categories (name, name_ar) VALUES 
    ('pediatric', 'أطفال'),
    ('adult', 'بالغين'),
    ('pregnant', 'حوامل'),
    ('dermatology', 'جلدية'),
    ('supplements', 'مكملات غذائية');

-- ===================================================================
-- 2. جدول أنواع الأدوية (Drug Types)
-- ===================================================================
CREATE TABLE IF NOT EXISTS drug_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    name_ar VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- إضافة بيانات أولية لأنواع الأدوية
INSERT INTO drug_types (name, name_ar) VALUES 
    ('antipyretics and analgesic', 'خافض حرارة ومسكن'),
    ('antihistamine and cortisone', 'مضاد هيستامين وكورتيزون'),
    ('antibiotic', 'مضاد حيوي'),
    ('GIT', 'جهاز هضمي'),
    ('respiratory tract', 'جهاز تنفسي'),
    ('NSAIDs', 'مضادات التهاب غير ستيرويدية');

-- ===================================================================
-- 3. جدول الشركات المصنعة (Manufacturers)
-- ===================================================================
CREATE TABLE IF NOT EXISTS manufacturers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL UNIQUE,
    name_ar VARCHAR(200),
    country VARCHAR(100),
    country_ar VARCHAR(100),
    website VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===================================================================
-- 4. جدول الأدوية (Medications) - محسّن ومفصّل
-- ===================================================================
CREATE TABLE IF NOT EXISTS medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- المعلومات الأساسية
    generic_name VARCHAR(200) NOT NULL,
    trade_name VARCHAR(200),
    category_id INTEGER,
    drug_type_id INTEGER,
    manufacturer_id INTEGER,
    
    -- معلومات الدواء
    concentration VARCHAR(100),
    form VARCHAR(100),
    active_ingredient TEXT,
    composition TEXT,
    
    -- الحدود العمرية
    min_age_months INTEGER,
    max_age_months INTEGER,
    age_limit_text VARCHAR(200),
    
    -- الحدود الوزنية
    min_weight_kg DECIMAL(5,2),
    max_weight_kg DECIMAL(5,2),
    weight_limit_text VARCHAR(200),
    
    -- معلومات الجرعة
    max_single_dose VARCHAR(100),
    dose_calculation TEXT,
    max_daily_dose VARCHAR(100),
    frequency VARCHAR(100),
    duration VARCHAR(100),
    administration_route VARCHAR(100),
    
    -- المعلومات الطبية والصيدلانية
    indications TEXT,
    contraindications TEXT,
    side_effects TEXT,
    drug_interactions TEXT,
    warnings TEXT,
    precautions TEXT,
    overdose_management TEXT,
    
    -- الحمل والرضاعة
    pregnancy_category VARCHAR(10),
    pregnancy_safety TEXT,
    lactation_safety TEXT,
    
    -- ظروف التخزين
    storage_conditions TEXT,
    shelf_life VARCHAR(100),
    storage_after_opening VARCHAR(100),
    
    -- معلومات تجارية
    warehouse_name VARCHAR(200),
    package_info VARCHAR(200),
    package_size VARCHAR(100),
    price DECIMAL(10,2),
    price_with_tax DECIMAL(10,2),
    availability VARCHAR(50),
    barcode VARCHAR(100),
    
    -- الصور والمستندات
    image_path VARCHAR(500),
    leaflet_path VARCHAR(500),
    box_image_path VARCHAR(500),
    additional_images TEXT,
    
    -- معلومات المنشأ
    manufacturing_country VARCHAR(100),
    marketing_country VARCHAR(100),
    license_number VARCHAR(100),
    
    -- ملاحظات وإضافات
    notes TEXT,
    pharmacist_notes TEXT,
    
    -- تواريخ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (drug_type_id) REFERENCES drug_types(id) ON DELETE SET NULL,
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id) ON DELETE SET NULL
);

-- ===================================================================
-- 5. جدول تقدير الأوزان حسب العمر (Age Weight Estimates)
-- ===================================================================
CREATE TABLE IF NOT EXISTS age_weight_estimates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age_months INTEGER NOT NULL UNIQUE,
    age_text VARCHAR(50) NOT NULL,
    estimated_weight_kg DECIMAL(5,2) NOT NULL,
    age_group VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- إضافة بيانات تقدير الأوزان (0-11 شهر)
INSERT INTO age_weight_estimates (age_months, age_text, estimated_weight_kg, age_group) VALUES 
    (1, '1 month', 4.4, '0-11 months'),
    (2, '2 month', 5.5, '0-11 months'),
    (3, '3 month', 6.2, '0-11 months'),
    (4, '4 month', 6.8, '0-11 months'),
    (5, '5 month', 7.3, '0-11 months'),
    (6, '6 month', 7.6, '0-11 months'),
    (7, '7 month', 8.1, '0-11 months'),
    (8, '8 month', 8.3, '0-11 months'),
    (9, '9 month', 8.6, '0-11 months'),
    (10, '10 month', 8.9, '0-11 months'),
    (11, '11 month', 9.2, '0-11 months');

-- إضافة بيانات تقدير الأوزان (1-5 سنوات)
INSERT INTO age_weight_estimates (age_months, age_text, estimated_weight_kg, age_group) VALUES 
    (12, '1 year', 9.5, '1-5 years'),
    (13, '13 month', 9.7, '1-5 years'),
    (14, '14 month', 9.9, '1-5 years'),
    (15, '15 month', 10.1, '1-5 years'),
    (16, '16 month', 10.3, '1-5 years'),
    (17, '17 month', 10.5, '1-5 years'),
    (18, '18 month', 10.7, '1-5 years'),
    (19, '19 month', 11.0, '1-5 years'),
    (20, '20 month', 11.2, '1-5 years'),
    (21, '21 month', 11.4, '1-5 years'),
    (22, '22 month', 11.6, '1-5 years'),
    (23, '23 month', 11.8, '1-5 years'),
    (24, '2 year', 12.2, '1-5 years'),
    (36, '3 year', 14.1, '1-5 years'),
    (48, '4 year', 15.8, '1-5 years'),
    (60, '5 year', 18.1, '1-5 years');

-- إضافة بيانات تقدير الأوزان (6-15 سنة)
INSERT INTO age_weight_estimates (age_months, age_text, estimated_weight_kg, age_group) VALUES 
    (72, '6 year', 20.3, '6-15 years'),
    (84, '7 year', 22.7, '6-15 years'),
    (96, '8 year', 25.7, '6-15 years'),
    (108, '9 year', 28.4, '6-15 years'),
    (120, '10 year', 32.0, '6-15 years'),
    (132, '11 year', 36.3, '6-15 years'),
    (144, '12 year', 40.7, '6-15 years'),
    (156, '13 year', 45.6, '6-15 years'),
    (168, '14 year', 49.2, '6-15 years'),
    (180, '15 year', 54.0, '6-15 years');

-- ===================================================================
-- 6. جدول سجل البحث (Search History) - اختياري
-- ===================================================================
CREATE TABLE IF NOT EXISTS search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    search_query VARCHAR(500),
    search_type VARCHAR(50),
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER
);

-- ===================================================================
-- الفهارس (Indexes) - لتحسين الأداء
-- ===================================================================
CREATE INDEX IF NOT EXISTS idx_medications_generic_name ON medications(generic_name);
CREATE INDEX IF NOT EXISTS idx_medications_trade_name ON medications(trade_name);
CREATE INDEX IF NOT EXISTS idx_medications_category ON medications(category_id);
CREATE INDEX IF NOT EXISTS idx_medications_drug_type ON medications(drug_type_id);
CREATE INDEX IF NOT EXISTS idx_medications_manufacturer ON medications(manufacturer_id);
CREATE INDEX IF NOT EXISTS idx_age_weight_estimates_age ON age_weight_estimates(age_months);
CREATE INDEX IF NOT EXISTS idx_manufacturers_name ON manufacturers(name);
CREATE INDEX IF NOT EXISTS idx_search_history_query ON search_history(search_query);

-- ===================================================================
-- Views (طرق عرض) - لتسهيل الاستعلامات
-- ===================================================================

-- عرض شامل للأدوية مع معلومات الفئة والشركة
CREATE VIEW IF NOT EXISTS medications_full_view AS
SELECT 
    m.*,
    c.name as category_name,
    c.name_ar as category_name_ar,
    dt.name as drug_type_name,
    dt.name_ar as drug_type_name_ar,
    mf.name as manufacturer_name,
    mf.country as manufacturer_country
FROM medications m
LEFT JOIN categories c ON m.category_id = c.id
LEFT JOIN drug_types dt ON m.drug_type_id = dt.id
LEFT JOIN manufacturers mf ON m.manufacturer_id = mf.id;

-- عرض للأدوية المتوفرة فقط
CREATE VIEW IF NOT EXISTS available_medications AS
SELECT * FROM medications_full_view
WHERE availability IN ('متوفر', 'available');

-- ===================================================================
-- Triggers (المحفزات) - للتحديث التلقائي
-- ===================================================================

-- تحديث حقل updated_at تلقائيًا عند تعديل الدواء
CREATE TRIGGER IF NOT EXISTS update_medication_timestamp 
AFTER UPDATE ON medications
FOR EACH ROW
BEGIN
    UPDATE medications SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- ===================================================================
-- نهاية ملف قاعدة البيانات
-- ===================================================================
