# Publish V1 to GitHub Pages when ready

Everything remains local. No branch was pushed and no site was deployed.

## One-time setup

1. From your original repository folder, confirm `git branch --show-current` says
   `v1`, then push when you choose: `git push -u origin v1`.
2. In GitHub, open repository **Settings → Pages → Build and deployment** and
   select **GitHub Actions** as the source. Private-repository Pages availability
   depends on your account plan; keep the assignment repository private.
3. Open **Actions → Publish V1 to GitHub Pages**. The first push runs this workflow;
   if it failed before Pages was enabled, rerun that workflow after step 2.
4. If GitHub blocks deployment because `v1` is not an allowed environment branch,
   open **Settings → Environments → github-pages** and allow `v1` under deployment
   branches, then rerun.
5. Use the successful deployment's actual URL. With the repository name unchanged
   and no custom domain, the expected V1 path is:
   `https://carlpatel.github.io/HW3-Spec-Driven-Development/v1/`.
   This is an expected address, not a claim that deployment is live.

The workflow runs on pushes to `v1`. Manual dispatch is also declared; GitHub's
Run workflow control requires the workflow to exist on the default branch, so
rerun the push-triggered run while the workflow exists only on `v1`.

## What gets published

The workflow tests, builds `dist/`, prepares `_site/v1/`, and uploads **only `_site/`**.
The repository root, interview transcripts, assignment PDFs, model files and
Spec Kit documents are not part of the Pages artifact. The root page redirects
to `./v1/`; all application assets and module imports use relative URLs, so the
repository-name subpath needs no configuration. No secrets or external services
are needed by the app. Reload resets mock data as specified.

To inspect the exact hosting artifact locally:

```sh
npm test
npm run build
node scripts/prepare-pages.mjs
```

Later V2 work must publish both `_site/v1/` and `_site/v2/` in one Pages deployment
if both URLs must remain available. A Pages deployment replaces the entire prior
artifact; preserve the frozen V1 build when adding V2.

References: [GitHub custom Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages),
[publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
