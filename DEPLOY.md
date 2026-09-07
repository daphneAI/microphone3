Deploy to Hugging Face Space

This repository can be pushed to a Hugging Face Space. The project includes a helper PowerShell script `deploy_to_space.ps1` and a GitHub Actions workflow that expects a repository secret named `space3Devices` containing a Hugging Face token with write access to the target Space.

Local deploy (quick)

1. Create a token at https://huggingface.co/settings/tokens with `write:repo` scope.
2. In PowerShell set the token in the environment and run the helper:

```powershell
$env:space3Devices = 'hf_xxx'
.\deploy_to_space.ps1
```

This force-pushes your current branch to `main` on the Space `daphneAI/space3Devices`.

CI deploy via GitHub Actions

1. In your GitHub repository, add a secret named `space3Devices` with the token value.
2. Push to the `main` branch; the workflow `.github/workflows/deploy-hf-space.yml` will run verification steps and deploy to the Space automatically.

Security note: Never commit tokens into the repository. Use GitHub Secrets or local environment variables when running scripts.
