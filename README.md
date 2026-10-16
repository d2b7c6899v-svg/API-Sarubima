# API Sarubima — Python/Kivy Starter

A small educational prototype for a Sri Lankan farmer-to-customer marketplace.

## Included
- Home screen with Farmer / Customer choices
- Farmer form to add produce (name, price/kg, quantity, farmer name)
- Customer marketplace with sample produce
- Basket with total calculation

## Limitations
This is a UI prototype. Products and basket are held in memory and reset when the app closes. Login, cloud database, photos, real orders, payments, and delivery are not implemented. Do not enter real passwords or sensitive personal information.

## Run on a computer
Install Python 3.10+ then run:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Android
Buildozer is usually used on Linux or a Linux cloud runner. After installing the current OS-specific Buildozer dependencies:

```bash
pip install buildozer
buildozer android debug
```

The first build downloads Android build tools and may take a while. The APK is normally created in `bin/`. Check the official Kivy/Buildozer docs for current dependencies.

## iPhone / iOS
Packaging Kivy for iOS normally requires a Mac and Apple's Xcode toolchain. An iPhone alone cannot compile this project into an iOS app. You can edit source files using an iPhone browser, but building and installing an iOS app requires a suitable Apple build environment.

## Suggested next steps
1. Add secure login and registration.
2. Add a FastAPI backend and database to sync products between devices.
3. Add product images, categories, search, and stock validation.
4. Add orders, delivery status, and a privacy policy before production use.


## Build APK using GitHub Actions from an iPhone

1. Create a GitHub repository named `API-Sarubima`.
2. Upload the contents of this folder to the repository root (including the hidden `.github` folder).
3. Open the repository's **Actions** tab and enable Actions if prompted.
4. Choose **Build API Sarubima Android APK** and tap **Run workflow**. If it does not appear, commit/push the files to the `main` branch and reload Actions.
5. Open the running workflow. Wait until all steps pass.
6. On the successful run page, find **Artifacts** and download `api-sarubima-debug-apk`.
7. The artifact is a ZIP file containing the APK. An APK cannot be installed on an iPhone; use an Android device to test it.

If a build fails, open the failed workflow and read the first red error step. Build dependencies can change, so a failed cloud build may need configuration updates.
