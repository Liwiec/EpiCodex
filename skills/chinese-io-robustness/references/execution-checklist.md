# Chinese IO Execution Checklist

- [ ] UTF-8 preflight variables set in the active shell.
- [ ] All file operations use `-LiteralPath` or `pathlib.Path`.
- [ ] Pre-scan finished with total file count and extension summary.
- [ ] Decode probe run on all target text files.
- [ ] Failed decodes moved to normalization flow, not skipped.
- [ ] Main pipeline completed on full file set.
- [ ] Repair queue processed and cleared.
- [ ] Output scan confirms no replacement character `�`.
- [ ] Final report includes processed count, repaired count, and unresolved count.

