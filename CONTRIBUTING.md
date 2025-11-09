# Contributing to molecule-proxmox-lxc

Thank you for considering contributing to molecule-proxmox-lxc!

## Development Setup

1. **Clone the repository:**
```bash
git clone https://github.com/filatof/molecule-proxmox-lxc
cd molecule-proxmox-lxc
```

2. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install in development mode:**
```bash
pip install -e ".[dev]"
```

## Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **Flake8** for linting
- **Pylint** for additional checks
- **MyPy** for type checking

### Format your code:
```bash
tox -e format
```

### Check formatting:
```bash
tox -e format-check
```

### Run linting:
```bash
tox -e lint
```

### Run type checking:
```bash
tox -e type
```

## Testing

### Run all tests:
```bash
tox
```

### Run tests for specific Python version:
```bash
tox -e py311
```

### Run tests with latest dependencies:
```bash
tox -e latest
```

## Making Changes

1. **Create a new branch:**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**

3. **Test your changes:**
```bash
tox
```

4. **Update CHANGELOG.md** under the `[Unreleased]` section

5. **Commit your changes:**
```bash
git add .
git commit -m "Description of your changes"
```

6. **Push to your fork:**
```bash
git push origin feature/your-feature-name
```

7. **Create a Pull Request**

## Pull Request Guidelines

- Write clear, descriptive commit messages
- Include tests for new features
- Update documentation as needed
- Ensure all tests pass
- Follow the existing code style
- Keep changes focused and atomic

## Reporting Bugs

Please use GitHub Issues and include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, Proxmox version)
- Relevant logs or error messages

## Feature Requests

We welcome feature requests! Please:
- Check if the feature already exists or is planned
- Clearly describe the use case
- Explain why it would be useful

## Code of Conduct

Be respectful and constructive in all interactions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.