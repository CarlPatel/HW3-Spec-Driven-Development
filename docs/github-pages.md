# Publish the V1/V2 comparison when ready

No push or deployment is performed by these instructions. Both apps run locally:
`npm start` → http://localhost:4183/; choose /v1/ or /v2/.

1. Push local branch v2 when ready: `git push -u origin v2`.
2. In Settings → Pages, choose GitHub Actions as source. The checked-in workflow
   `.github/workflows/pages.yml` now runs on pushes to v2 and publishes BOTH versions.
3. If the github-pages environment restricts branches, allow v2 in that environment.
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

The older workflow on branch v1 publishes only V1. Avoid pushing/rerunning that
workflow after the comparison is deployed, since a Pages artifact replaces the whole
site. Publish subsequent updates from the combined v2 workflow. When merging into
main for submission, update the workflow branch trigger to main (and avoid competing
publishing workflows) so the default README and Pages workflow stay consistent.

The default README must link actual successful deployment URLs and both source refs.
No live V2 deployment is claimed here. Private-repository Pages availability depends
on the account plan; do not change repository visibility automatically.
