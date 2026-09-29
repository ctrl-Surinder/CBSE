import os
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont


# ============================================================
# CBSE STUDENT PHOTO PROCESSOR
# ============================================================

# Photograph: 3.5 cm x 4.5 cm at 300 DPI
PHOTO_WIDTH = 413
PHOTO_HEIGHT = 531
DPI = 300

# Final JPG file size
MIN_KB = 10
MAX_KB = 40

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


# ============================================================
# ASK FOR DATE
# ============================================================

def ask_date():

    while True:

        date = input(
            "Enter photograph date (DD/MM/YYYY): "
        ).strip()

        parts = date.split("/")

        if len(parts) == 3:

            try:

                day = int(parts[0])
                month = int(parts[1])
                year = int(parts[2])

                if (
                    1 <= day <= 31
                    and 1 <= month <= 12
                    and len(parts[2]) == 4
                    and 1900 <= year <= 2100
                ):

                    return (
                        f"{day:02d}/"
                        f"{month:02d}/"
                        f"{year:04d}"
                    )

            except ValueError:
                pass

        print(
            "Invalid date. "
            "Please enter DD/MM/YYYY."
        )


# ============================================================
# ASK FOR TEXT SIZE
# ============================================================

def ask_text_size():

    print()
    print("=" * 50)
    print("Choose name/date text size")
    print("=" * 50)

    print()
    print("1. Small       - Name 18 px / Date 16 px")
    print("2. Medium      - Name 22 px / Date 20 px")
    print("3. Large       - Name 26 px / Date 23 px")
    print("4. Extra Large - Name 30 px / Date 27 px")
    print("5. Custom      - Choose your own size")
    print()

    while True:

        choice = input(
            "Enter choice [1-5]: "
        ).strip()

        if choice == "1":
            return 18, 16

        elif choice == "2":
            return 22, 20

        elif choice == "3":
            return 26, 23

        elif choice == "4":
            return 30, 27

        elif choice == "5":

            while True:

                try:

                    name_size = int(
                        input(
                            "Enter student name "
                            "font size in pixels: "
                        )
                    )

                    if 10 <= name_size <= 60:
                        break

                    print(
                        "Please choose a size "
                        "between 10 and 60."
                    )

                except ValueError:

                    print(
                        "Please enter a number."
                    )

            while True:

                try:

                    date_size = int(
                        input(
                            "Enter date font size "
                            f"in pixels "
                            "(recommended {max(10, name_size - 3)}): "
                        )
                    )

                    if 10 <= date_size <= 60:
                        break

                    print(
                        "Please choose a size "
                        "between 10 and 60."
                    )

                except ValueError:

                    print(
                        "Please enter a number."
                    )

            return name_size, date_size

        else:

            print(
                "Please enter 1, 2, 3, 4 or 5."
            )


# ============================================================
# FIND WINDOWS FONT
# ============================================================

def get_font(size):

    font_paths = [

        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\Arial.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
        r"C:\Windows\Fonts\Calibri.ttf",

    ]

    for path in font_paths:

        if os.path.exists(path):

            try:

                return ImageFont.truetype(
                    path,
                    size
                )

            except Exception:
                pass

    return ImageFont.load_default()


# ============================================================
# CROP AND RESIZE PHOTOGRAPH
# ============================================================

def prepare_photo(image):

    image = ImageOps.exif_transpose(image)

    image = image.convert("RGB")

    target_ratio = (
        PHOTO_WIDTH / PHOTO_HEIGHT
    )

    current_ratio = (
        image.width / image.height
    )

    # Too wide
    if current_ratio > target_ratio:

        new_width = int(
            image.height * target_ratio
        )

        left = (
            image.width - new_width
        ) // 2

        image = image.crop(
            (
                left,
                0,
                left + new_width,
                image.height
            )
        )

    # Too tall
    elif current_ratio < target_ratio:

        new_height = int(
            image.width / target_ratio
        )

        top = (
            image.height - new_height
        ) // 2

        image = image.crop(
            (
                0,
                top,
                image.width,
                top + new_height
            )
        )

    # Exact required photograph size
    image = image.resize(
        (
            PHOTO_WIDTH,
            PHOTO_HEIGHT
        ),
        Image.Resampling.LANCZOS
    )

    return image


# ============================================================
# CREATE PHOTO 2
# ============================================================

def create_photo_2(
    photo,
    student_name,
    date,
    name_font_size,
    date_font_size
):

    name_font = get_font(
        name_font_size
    )

    date_font = get_font(
        date_font_size
    )

    # Measure text
    temp = Image.new(
        "RGB",
        (PHOTO_WIDTH, 100),
        "white"
    )

    draw = ImageDraw.Draw(temp)

    name_box = draw.textbbox(
        (0, 0),
        student_name,
        font=name_font
    )

    date_box = draw.textbbox(
        (0, 0),
        date,
        font=date_font
    )

    name_height = (
        name_box[3] - name_box[1]
    )

    date_height = (
        date_box[3] - date_box[1]
    )

    # Calculate required text area dynamically
    top_margin = 8
    gap = 6
    bottom_margin = 8

    text_area_height = (
        top_margin
        + name_height
        + gap
        + date_height
        + bottom_margin
    )

    # Final image
    canvas_height = (
        PHOTO_HEIGHT
        + text_area_height
    )

    canvas = Image.new(
        "RGB",
        (
            PHOTO_WIDTH,
            canvas_height
        ),
        "white"
    )

    # IMPORTANT:
    # Photograph remains exactly 413 x 531 pixels.
    canvas.paste(
        photo,
        (0, 0)
    )

    draw = ImageDraw.Draw(
        canvas
    )

    # --------------------------------------------------------
    # NAME
    # --------------------------------------------------------

    name_box = draw.textbbox(
        (0, 0),
        student_name,
        font=name_font
    )

    name_width = (
        name_box[2] - name_box[0]
    )

    name_x = (
        PHOTO_WIDTH - name_width
    ) // 2

    name_y = (
        PHOTO_HEIGHT
        + top_margin
    )

    draw.text(
        (
            name_x,
            name_y
        ),
        student_name,
        fill="black",
        font=name_font
    )

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    date_box = draw.textbbox(
        (0, 0),
        date,
        font=date_font
    )

    date_width = (
        date_box[2] - date_box[0]
    )

    date_y = (
        name_y
        + name_height
        + gap
    )

    date_x = (
        PHOTO_WIDTH - date_width
    ) // 2

    draw.text(
        (
            date_x,
            date_y
        ),
        date,
        fill="black",
        font=date_font
    )

    return canvas


# ============================================================
# SAVE JPG BETWEEN 10 AND 40 KB
# ============================================================

def save_jpg_with_size_limit(
    image,
    output_file
):

    for quality in range(
        95,
        9,
        -2
    ):

        image.save(
            output_file,
            "JPEG",
            quality=quality,
            optimize=True,
            progressive=False,
            dpi=(DPI, DPI)
        )

        size_kb = (
            output_file.stat().st_size
            / 1024
        )

        if (
            MIN_KB
            <= size_kb
            <= MAX_KB
        ):

            return True, size_kb

    size_kb = (
        output_file.stat().st_size
        / 1024
    )

    return False, size_kb


# ============================================================
# PROCESS ONE STUDENT
# ============================================================

def process_student(
    input_file,
    photo1_folder,
    photo2_folder,
    date,
    name_font_size,
    date_font_size
):

    student_name = (
        input_file.stem.strip()
    )

    print()
    print("-" * 55)
    print(
        "Processing:",
        student_name
    )

    try:

        with Image.open(
            input_file
        ) as original:

            # ================================================
            # PREPARE PHOTO
            # ================================================

            photo = prepare_photo(
                original
            )

            # ================================================
            # PHOTO 1
            # ================================================

            photo1_file = (
                photo1_folder
                / f"{student_name}_1.jpg"
            )

            success1, size1 = (
                save_jpg_with_size_limit(
                    photo,
                    photo1_file
                )
            )

            # ================================================
            # PHOTO 2
            # ================================================

            photo2 = create_photo_2(
                photo,
                student_name,
                date,
                name_font_size,
                date_font_size
            )

            photo2_file = (
                photo2_folder
                / f"{student_name}_2.jpg"
            )

            success2, size2 = (
                save_jpg_with_size_limit(
                    photo2,
                    photo2_file
                )
            )

            print(
                f"Photo 1: {size1:.1f} KB"
            )

            print(
                f"Photo 2: {size2:.1f} KB"
            )

            if success1 and success2:

                print("STATUS: OK")

                return True

            else:

                print(
                    "STATUS: CHECK FILE SIZE"
                )

                return False

    except Exception as error:

        print(
            "ERROR:",
            error
        )

        return False


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print(" CBSE REGISTRATION & LOC")
    print(" STUDENT PHOTOGRAPH PROCESSOR")
    print("=" * 60)

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    print()

    date = ask_date()

    # --------------------------------------------------------
    # TEXT SIZE
    # --------------------------------------------------------

    name_font_size, date_font_size = (
        ask_text_size()
    )

    print()
    print(
        f"Selected name size: "
        f"{name_font_size}px"
    )

    print(
        f"Selected date size: "
        f"{date_font_size}px"
    )

    # --------------------------------------------------------
    # INPUT FOLDER
    # --------------------------------------------------------

    print()

    input_folder = input(
        "Enter the folder containing "
        "the original student photographs:\n"
    ).strip().strip('"')

    input_path = Path(
        input_folder
    )

    if not input_path.exists():

        print()
        print(
            "ERROR: Folder does not exist."
        )

        input(
            "Press Enter to exit..."
        )

        return

    # --------------------------------------------------------
    # OUTPUT FOLDERS
    # --------------------------------------------------------

    output_root = (
        input_path / "Processed"
    )

    photo1_folder = (
        output_root
        / "Photo 1 - Plain"
    )

    photo2_folder = (
        output_root
        / "Photo 2 - Name & Date"
    )

    photo1_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    photo2_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # FIND INPUT PHOTOS
    # --------------------------------------------------------

    files = []

    for file in input_path.iterdir():

        if (
            file.is_file()
            and file.suffix.lower()
            in SUPPORTED_EXTENSIONS
        ):

            # Don't process generated files
            if file.stem.endswith("_1"):
                continue

            if file.stem.endswith("_2"):
                continue

            files.append(file)

    files.sort(
        key=lambda x: x.name.lower()
    )

    if not files:

        print()
        print(
            "No photographs found."
        )

        input(
            "Press Enter to exit..."
        )

        return

    # --------------------------------------------------------
    # PROCESS ALL STUDENTS
    # --------------------------------------------------------

    successful = 0
    failed = 0

    print()
    print(
        f"Found {len(files)} photograph(s)."
    )

    for file in files:

        result = process_student(
            file,
            photo1_folder,
            photo2_folder,
            date,
            name_font_size,
            date_font_size
        )

        if result:
            successful += 1
        else:
            failed += 1

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)

    print(
        f"Successfully processed: "
        f"{successful}"
    )

    print(
        f"Needs checking: "
        f"{failed}"
    )

    print()
    print(
        "Output folder:"
    )

    print(output_root)

    print()
    print(
        "Photo 1 - Plain:"
    )

    print(photo1_folder)

    print()
    print(
        "Photo 2 - Name & Date:"
    )

    print(photo2_folder)

    print()

    input(
        "Press Enter to close..."
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()