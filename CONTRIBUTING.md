# Contributing to Ghost JSON Media Extractor

Thank you for your interest in contributing! This guide will help you get started.

## Reporting Bugs

If you find a bug, please [open an issue](https://github.com/codeme-ne/ghost-blog-json-image/issues) with:

- **Description**: What happened vs what you expected
- **Ghost version**: Which Ghost version created your export
- **Python version**: Run `python --version`
- **Steps to reproduce**: Detailed steps to trigger the bug
- **Error messages**: Full error output if applicable
- **Sample export**: If possible, a minimal anonymized Ghost export that reproduces the issue

## Requesting Features

Have an idea? [Open an issue](https://github.com/codeme-ne/ghost-blog-json-image/issues) with:

- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives considered**: Other approaches you've thought about

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/codeme-ne/ghost-blog-json-image.git
   cd ghost-blog-json-image
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test with sample export**
   ```bash
   python extract_media.py examples/ghost-export-sample.json --blog-url https://example.com --dry-run
   ```

## Code Style

This project follows simple Python conventions:

- **Naming**: `snake_case` for functions/variables, `UPPERCASE` for constants
- **Docstrings**: Google-style docstrings for all functions
- **Formatting**: f-strings for string formatting
- **Line length**: Keep it reasonable (~100 chars)
- **Comments**: Explain *why*, not *what*

## Testing

Currently, testing is manual:

1. Run with the sample export file in `examples/`
2. Test with `--dry-run` first to verify URL parsing
3. Verify actual downloads work correctly
4. Test edge cases (missing fields, malformed URLs, etc.)

Future: Automated tests with pytest would be welcome!

## Submitting Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style above
   - Add docstrings for new functions
   - Test thoroughly with sample exports

4. **Commit with clear messages**
   ```bash
   git commit -m "feat: add support for Ghost 5.x exports"
   git commit -m "fix: handle missing feature_image gracefully"
   git commit -m "docs: update README with new examples"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a pull request on GitHub

6. **PR checklist**:
   - [ ] Code follows existing style
   - [ ] Docstrings added/updated
   - [ ] Tested manually with sample export
   - [ ] README updated if user-facing changes
   - [ ] No breaking changes (or clearly documented)

## Areas for Contribution

Some ideas if you're looking to contribute:

- **Automated tests**: Add pytest test suite
- **Ghost version compatibility**: Test with different Ghost versions
- **Performance**: Optimize download speed or memory usage
- **Error handling**: Better error messages for edge cases
- **Features**: Support for different Ghost export formats
- **Documentation**: Improve README, add examples, create video tutorial

## Questions?

Open an issue for questions or join the discussion in existing issues!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
