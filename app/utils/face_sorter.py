import os
import shutil
import face_recognition


def sort_images(input_dir: str, output_dir: str) -> int:
    known_persons = []
    person_folders = []
    total_faces = 0

    def create_person_folder(idx: int):
        folder = os.path.join(output_dir, f"person_{idx}")
        os.makedirs(folder, exist_ok=True)
        return folder

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        path = os.path.join(input_dir, filename)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        total_faces += len(encodings)

        if not encodings:
            continue

        matched_indices = []

        for enc in encodings:
            match_found = False

            for idx, person_embeds in enumerate(known_persons):
                if True in face_recognition.compare_faces(
                    person_embeds, enc, tolerance=0.5
                ):
                    person_embeds.append(enc)
                    matched_indices.append(idx)
                    match_found = True
                    break

            if not match_found:
                new_idx = len(known_persons)
                known_persons.append([enc])
                person_folders.append(create_person_folder(new_idx))
                matched_indices.append(new_idx)

        for idx in matched_indices:
            shutil.copy(path, os.path.join(person_folders[idx], filename))

    return total_faces