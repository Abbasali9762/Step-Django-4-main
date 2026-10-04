# Dərs 9 — Model, migration, ORM və admin

> **Canlı kodu yazarkən `ADDIMLAR.pdf`-ə bax** — orada hər addımda hansı faylda hansı sətirləri yazacağın
> yaşıl rənglə (silinənlər qırmızı) göstərilib, terminal çıxışları real yoxlanılıb. Bu fayl isə dərsin qısa xəritəsidir.
> **Vacib ardıcıllıq:** `data.py` → baza köçürməsi shell-in **ən əvvəlində** edilir (slayd 24, ADDIMLAR addım 8),
> sorğular ondan sonra. Səbəb: postların id-ləri `data.py`-dakı 1–5 ilə eyni olmalıdır — kateqoriya/müəllif/latest
> səhifələri hələ `data.py`-dan oxuyur və `/post/1/`… linkləri verir. Admin-də “Əlavə et” formasını göstər, amma **saxlama**.

> **Arxa monitor üçün.** Bu qovluq dərsin SONUNDAKI tam layihədir.
> Kodda nişanlar: `[DƏRS 9]` = sən yazırsan · `[PRAKTİKA 9]` = tələbə yazır · `[EV 9]` = ev tapşırığı.
> Köhnə nişanlar (`[DƏRS 8]`, `[EV 8]`) template-lərdədir — o sətirlər hansı dərsdə yarandığını göstərir.
> I hissədə yalnız `[DƏRS 9]` sətirlərini yaz. `is_featured`, `list_editable`, `actions`, baxış sayğacı → ev tapşırığıdır, dərsdə YAZMA.

**Dərsin sonunda:** postlar və kateqoriyalar bazadadır, admin paneldən idarə olunur.
`/`, `/post/<id>/`, `/categories/`, `/category/<slug>/` bazadan oxuyur.
`/author/`, `/latest/`, `/stats/` hələ `data.py`-dan oxuyur — ona görə **`data.py` dərsdə SİLİNMİR** (ev tapşırığı 7).

Migration tarixçəsi (tələbədə də belə olmalıdır):
`0001_initial` (Post — sən) → `0002_category` (Category — praktika) → `0003_post_is_featured` (ev).

## Bu layihəni işə salmaq (standart qayda)
```bash
cd project/django/lesson-09
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate           # bazanı yarat
python manage.py loaddata demo     # 5 post + 3 kateqoriya (yalnız sənin üçün — tələbəyə göstərilmir)
python manage.py createsuperuser   # admin panel üçün, bir dəfəlik
python manage.py runserver         # → http://127.0.0.1:8000
```

---

## Vaxt planı

| Vaxt | Nə | Slayd | ADDIMLAR |
|---|---|---|---|
| 0:00–0:10 | Keçən dərsdən 5 sual + ev tapşırığına baxış. Problem: `data.py` niyə bəs etmir | 1–4 | 2 |
| 0:10–0:20 | Baza = Excel cədvəli, SQLite, ORM ideyası, SQL vs ORM | 5–8 | 2 |
| 0:20–0:40 | **CANLI:** `Post` modeli sahə-sahə, `Meta`, `__str__`, null/blank, müvəqqəti sahələr | 9–15 | 3 |
| 0:40–0:50 | **CANLI:** `makemigrations` → `migrate`, migration faylına baxış, “no such table” | 16–19 | 4 |
| 0:50–1:00 | **CANLI:** `createsuperuser`, `PostAdmin` | 20–22 | 5–7 |
| 1:00–1:15 | **CANLI:** shell — create, filter, get, save, delete. Mikro-tapşırıq. `data.py` → baza | 23–29 | 8–13 |
| 1:15–1:30 | **CANLI:** view-lar bazadan, `get_object_or_404`, template-lər toxunulmur, xəta cədvəli | 30–34 | 14–17 |
| 1:30–1:40 | **Fasilə** | | |
| 1:40–2:50 | **PRAKTİKA:** 3 blok × ~22 dəq, hər blokun sonunda checkpoint | 35–39 | 18 |
| 2:50–3:00 | Son push, ev tapşırığı vərəqi, Dərs 10 anonsu | 40 | 19–20 |

---

## Dərsdən əvvəl (5 dəq)
Tələbələr Dərs 8-in sonundakı layihəni clone edir:
```bash
git clone <repo> && cd step-blog
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver        # Dərs 8-dəki sayt açılmalıdır
```
⚠ `runserver` “You have 18 unapplied migration(s)” yazır — **indi toxunma**, bu gün məhz bunu həll edəcəyik.

---

## CANLI KOD — addım-addım

### Addım 1 — problem (0:05)
Soruş: “Yeni post yazmaq üçün nə etməliyik?” → `data.py`-ı açıb kod dəyişmək.
“Müəllim deyil, redaktor post yazmalıdır. O Python bilmir.” → baza + admin.

### Addım 2 — ORM ideyası (0:10)
Lövhədə üç sütun çək: **class ↔ cədvəl · atribut ↔ sütun · obyekt ↔ sətir**.
**De:** “Dərs 3-də `Telebe` class-ı yazırdıq, obyektlər yaddaşda yaşayırdı, proqram bağlananda ölürdü.
İndi class eynidir, sadəcə obyektlər bazada yaşayır.”

### Addım 3 — Post modeli (0:20)
`blog/models.py` → `Post` (fayldakı `[DƏRS 9]` hissəsi, **`is_featured` olmadan**).
Sahə-sahə yaz, hər birində dayan:
- `CharField(max_length=200)` — **De:** “max_length = maksimum simvol sayı. Həmişə yazırıq — bəzi bazalar (MySQL) onsuz işləmir.”
- `TextField` — limitsiz.
- `BooleanField(default=True)`, `PositiveIntegerField(default=0)` — “default = dəyər verilməsə nə yazılsın.”
- `DateTimeField(auto_now_add=True)` — “yaranan an özü yazılır, sən toxunmursan.”
- `class Meta: ordering = ["-created_at"]`, `__str__`.

**De (vacib!):** “`author` və `category` hələlik adi mətndir. Bu **bilə-bilə** müvəqqəti həlldir.
Admin-də `oyunlr` yazsan, heç kim səni saxlamayacaq. Dərs 10-da bunu düzəldəcəyik.” → bu, gələn dərsin motivasiyasıdır.

**De:** “Sahə adlarına bax: `title`, `author`, `category`, `content`, `created_at` — `data.py`-dakı açarların eynisi. Bu təsadüf deyil.”

### Addım 4 — migration (0:40)
```bash
python manage.py makemigrations    # → blog/migrations/0001_initial.py
python manage.py migrate           # Django-nun öz cədvəlləri + blog_post
```
`0001_initial.py` faylını aç, 10 saniyə göstər: “Bu bizim model-in təsviridir. Əl ilə dəyişmirik.”
**De:** “Migration = bazanın git commit-i. Model dəyişdi → iki komanda. Həmişə.”

⚠ Əvvəlcə **yalnız `makemigrations`** et, sonra saytı aç → `no such table: blog_post` göstərməyə ehtiyac yoxdur,
çünki view-lar hələ `data.py`-dan oxuyur. Bu xətanı Addım 7-də, view-u dəyişəndən sonra göstərmək olar (istəsən).

### Addım 5 — admin (0:50)
```bash
python manage.py createsuperuser   # admin / parol — ekranda görünmür, normaldır
```
`blog/admin.py` → əvvəlcə `admin.site.register(Post)` yaz. `/admin/` aç → Posts → “Əlavə et” formasını **göstər, saxlama**
(id-lər 1–5 `data.py` ilə üst-üstə düşməlidir — köçürmə növbəti addımdadır).
Sonra `@admin.register(Post)` + `PostAdmin` (`list_display`, `list_filter`, `search_fields`) — fayldakı `[DƏRS 9]` hissəsi,
amma **`is_featured`, `list_editable`, `actions` olmadan**:
```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "is_published", "views", "created_at"]
    list_filter = ["is_published", "category"]
    search_fields = ["title", "content"]
```
**De:** “Dərs 4 — `PostAdmin` `ModelAdmin`-dən törəyir. Biz yalnız bir neçə atributu override edirik.”
**Göstər:** `__str__`-i müvəqqəti sil → admin-də `Post object (1)`. Geri qaytar.

⚠ `admin.site.register(Post)` sətrini silməyi unudan olacaq → `AlreadyRegistered`.

### Addım 6 — shell (1:00)
```bash
python manage.py shell
```
```python
# 1) ƏVVƏLCƏ data.py → baza (slayd 24) — id-lər 1–5 olur
from blog.models import Post
from blog.data import POSTS
for p in POSTS:
    Post.objects.create(title=p["title"], author=p["author"], category=p["category"], content=p["content"])

# 2) sonra sorğular (slayd 25–28)
Post.objects.all()
Post.objects.count()
Post.objects.filter(author="nigar")
Post.objects.exclude(category="oyunlar")
Post.objects.order_by("-views")
Post.objects.order_by("-views").first()
Post.objects.all()[:3]

p = Post.objects.get(id=1)
p.title = "Yeni başlıq"
p.save()                            # admin-də yoxla — dəyişdi

Post.objects.get(id=999)            # DoesNotExist — göstər
Post.objects.filter(id=1).title     # AttributeError — filter QuerySet qaytarır
```
**Mikro (5 dəq):** slayd 29 — 5 sorğu.

### Addım 7 — data.py → baza (1:10)
Admin-də əl ilə yaratdığın test postunu sil (və ya saxla — fərq etmir). Sonra shell-də:
```python
from blog.models import Post
from blog.data import POSTS

for p in POSTS:
    Post.objects.create(title=p["title"], author=p["author"], category=p["category"], content=p["content"])

Post.objects.count()    # 5
```
**De:** “`created_at` vermədik — `auto_now_add` onsuz da qəbul etmir. Hamısı indiki vaxtı aldı.”

🆘 **Ehtiyat plan** (shell alınmasa, vaxt gedirsə): `python manage.py loaddata demo`
(`blog/fixtures/demo.json` — 5 post + 3 kateqoriya, tarixləri ilə). ⚠ Bu fixture-da kateqoriyalar da var —
praktikadan ƏVVƏL işlətsən, `0002_category` migration-u olmadığı üçün xəta verəcək. Yalnız öz demonstrasiya bazanda,
praktikadan sonra işlət. Tələbəyə göstərmə.

### Addım 8 — view-lar bazadan (1:15)
`blog/views.py`: `from .models import Post` + `from django.shortcuts import get_object_or_404`.
1. `post_list` → `Post.objects.filter(is_published=True)`.
2. `post_detail` → `get_object_or_404(Post, id=post_id, is_published=True)`.
   Əvvəlcə `Post.objects.get(id=post_id)` yaz → `/post/99/` → 500 (DoesNotExist). Sonra `get_object_or_404` → 404.
3. Admin-də bir postu “dərc olunmayıb” et → siyahıdan itdi. `/post/<id>/` ilə aç → 404. “Filtr detalda da lazımdır.”
4. `data.py` importunu hələ **saxla** (`category_list` və ev view-ları ondan istifadə edir).

**Göstər:** template-lərdə **heç nə dəyişmədi**, sayt eyni görünür. **De:** “Məlumatın mənbəyi dəyişdi, görünüş xəbər tutmadı. MVT budur.”

⚠ `created_at` indi `datetime`-dır, `date` deyil — `|date:"d.m.Y"` eyni işləyir, heç nə etmə.

---

## PRAKTİKA — tələbə kateqoriyaları bazaya köçürür

| Blok | Tapşırıq | Checkpoint (ekranda yoxla) |
|---|---|---|
| A (~22 dəq) | `Category` modeli (`name`, `slug` unique, `description` blank) + `Meta` + `__str__` + `makemigrations`/`migrate` | `0002_category.py` yarandı, `migrate` OK |
| B (~22 dəq) | `CategoryAdmin` (`list_display`, `prepopulated_fields`) + shell-də `CATEGORIES` import | Admin-də 3 kateqoriya adı ilə; yeni əlavə edəndə slug özü dolur |
| C (~22 dəq) | `category_list` / `category_detail` ORM ilə, `get_object_or_404`, `Post.objects.filter(category=slug, is_published=True)` + push | `/category/oyunlar/` 2 post, `/category/futbol/` 404 |

**Qaydan:** yeni heç nə izah etmə. Tələbəyə de: “`Post` üçün nə etdiksə, eynisi. Öz `models.py` və `admin.py`-na bax.”

Shell importu (tələbə özü yazmalıdır, ilişən olsa göstər):
```python
from blog.models import Category
from blog.data import CATEGORIES

for c in CATEGORIES:
    Category.objects.create(name=c["name"], slug=c["slug"], description=c["description"])
```

### Tez-tez çıxan xətalar (praktikada)
| Xəta | Səbəb |
|---|---|
| `no such table: blog_category` | `makemigrations` + `migrate` edilməyib |
| `No changes detected` | `models.py` saxlanmayıb |
| `UNIQUE constraint failed: blog_category.slug` | shell importu iki dəfə işlədilib — `Category.objects.all().delete()` et, yenidən |
| Admin-də `Categorys` | `verbose_name_plural` yazılmayıb |
| Admin-də `Category object (1)` | `__str__` yoxdur |
| Admin-də `Category` görünmür | `admin.py`-da register yoxdur, ya da `from .models import Category` unudulub |
| `Category matching query does not exist` | view-da `get()` — `get_object_or_404` işlət |
| `/category/oyunlar/` boşdur | `filter(category=...)`-ə kateqoriya **obyekti** verilib, slug yox (`category=slug`) |

---

## Növbəti dərsə körpü
Admin-də bir postun kateqoriyasını `oyunlr` yaz → kart linki `/category/oyunlr/` → 404.
Soruş: “Kateqoriyanın adını `Oyunlar` → `Video oyunlar` etsək, postlarda nə olacaq?”
→ Dərs 10: `ForeignKey`. Post kateqoriyanın **özünə** bağlanacaq, mətnə yox.
