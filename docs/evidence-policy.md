# Publication and evidence policy

The private academic reports were read in full: eight pages for Star Wars and nine for Among Us.
They are co-authored technical evidence, not ranking certificates. Neither PDF is included here.
The 3rd-place result is separately attributed to the participant's statement.

Removed from publication: original infrastructure address/ports, cookies, session IDs, credentials,
private signing material, original flags, unpublished artifacts and screenshots of restricted systems.
No original author email, colleague identity or unrelated personal information is needed for the demos.

Public code is newly reconstructed with AI assistance. The examples use tiny, synthetic RSA values,
fictional events and generated LSB samples. The README image is rendered from actual local demo
output and labeled synthetic. It is not a screenshot of the competition.

Corrections to the source interpretation: RSA public parameters need not be secret; decoding a JWT
does not verify it; recovering a public modulus does not forge signatures; a failed route must not be
presented as a success; the unknown derivation does not prove the original challenge was impossible.

## Reproducibility checklist

- Python 3.11+ and standard library only.
- Each demo runs without internet access or an application server.
- Tests cover successful and rejected inputs and the partial-result invariant.
- Original PDFs, runtime reports, raw evidence and secrets are ignored by Git.
- Original code and summaries are MIT; original challenge content remains outside this license.
