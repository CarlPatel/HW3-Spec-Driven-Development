# Publish the V1/V2 comparison when ready

The submission workflow publishes both versions from main. Both apps also run locally:
`npm start` → http://localhost:4183/; choose /v1/ or /v2/.

1. Publish reviewed submission updates with `git push origin main`.
2. In Settings → Pages, choose GitHub Actions as source. The checked-in workflow
   `.github/workflows/pages.yml` now runs on pushes to main and publishes BOTH versions.
3. If the github-pages environment restricts branches, allow main in that environment.
4. Rerun the push-triggered workflow if initial setup blocked it. Manual dispatch
   becomes available once this workflow also exists on the default branch.
5. Verify the actual deployment output. Expected URLs for this unchanged repository:
   - https://carlpatel.github.io/HW3-Spec-Driven-Development/v1/
   - https://carlpatel.github.io/HW3-Spec-Driven-Development/v2/

Only the built comparison index and app assets are uploaded from `_site/`. Class
PDFs, interviews, specs and evaluation evidence are excluded. Asset/module URLs are
relative and work under the repository subpath. `npm run build` validates V1 frozen
checksums and generates dist/v1 and dist/v2; `node scripts/prepare-pages.mjs` copies
that entire output to _site. Never deploy just one version over the other.

The older branch workflows can publish stale content if manually rerun or pushed.
Use the combined main workflow for the submission. Both v1 and v2 branches remain
preserved as source versions; main contains the complete submission and learning log.

Pages publishes only `_site/`; repository access is separate. Keep the assignment
repository private and grant the instructor read access if they do not already have it.
