# Reference-folder inventory and retention record

This inventory was made before deleting `week5/`, `week9/` and `Lab Instructions/`.
All 33 files were accounted for while the folders still existed. The root
implementation and its tests were then validated before removal. Earlier tracked
weekly files remain available in Git at commit `e90b855`; no history is rewritten.

Categories: **A** obsolete/generated reference; **B** implementation merged;
**C** tests retained; **D** documentation retained; **E** assessment evidence retained;
**F** duplicate of retained material. The original broken tests were already
preserved in `test_expenses_original.py.txt` before this consolidation.

The lab PNGs were supplied reference screenshots, not the student's diagrams or
research answers. Their requirements were extracted into `../LAB_REVIEW.md`
before removal. The background lecture pages were reviewed and classified too.
The two coursework JPG diagrams remain at the root without alteration.

| Source file | Decision before removal | Original SHA-256 |
| --- | --- | --- |
| `week5/__pycache__/expenses.cpython-314.pyc` | A — Generated Python bytecode; source/tests retained at root; safe to regenerate. | `cc2364af4c05b23e2b99595bdbdf930d5b84f80ddd20eddc2ea060c41ea87e30` |
| `week5/__pycache__/test_expenses.cpython-314.pyc` | A — Generated Python bytecode; source/tests retained at root; safe to regenerate. | `40155a7d407083d13a95a4cdeb0b8bbf8d3e4d9e66d6a51b8c24e19da380df60` |
| `week5/__pycache__/test_expenses_given.cpython-314.pyc` | A — Generated Python bytecode; source/tests retained at root; safe to regenerate. | `ae88d7ba92817e88f6edbbbf96aed99cd3595fe34c336afad01ad5671df17cff` |
| `week5/expensediagram.jpg` | F — Byte-identical original diagram retained as root expensediagram.jpg. | `1ad2e08e2f160f1e2a161213a470f4565d71e2dd23957904268431b97ec18cbf` |
| `week5/expensediagramfinal.jpg` | F — Byte-identical final JPG retained as root expensediagramfinal.jpg; outstanding manual corrections documented. | `34120ff7ef0a1599f48c2a4626239c49acbad76a5c087d876d9121a4ace9e2c0` |
| `week5/expenses.csv` | F — Same header-only contents as root expenses.csv; only original line endings differ. Root file left untouched. | `a9776c44a8720c95c4f18cae2a736b954116912bfc4ffc479bb839dc430bcef9` |
| `week5/expenses.py` | B — Baseline compared with the corrected root implementation; original retained in Git at e90b855. | `ed115a3ffbe1e7784e728424de760e7e897c7a4db2fa8eb33bd0e3be17da8f7a` |
| `week5/test_expenses.py` | C — All 67 test methods retained in root test_expenses.py; refusal/message expectations adapted to the final behaviour. | `4dc0a771a06b9a471c8ca292817caea7d3855d7d319cea5cad001075ac5804cc` |
| `week5/test_expenses_given.py` | F — Byte-identical to retained root test_expenses_given.py. | `b95a0520b5e2c0b944897bb486161a801b6934b161ec30cef8f1937cf3dc96e1` |
| `week9/__pycache__/expenses.cpython-314.pyc` | A — Generated Python bytecode; source/tests retained at root; safe to regenerate. | `09528c504717245787b9bc362f6f8874c17b02fb00d9d27307583468660e7f43` |
| `week9/__pycache__/test_expenses.cpython-314.pyc` | A — Generated Python bytecode; source/tests retained at root; safe to regenerate. | `857832dbba7a3367c6e126ccc00aca0d7a5cdeea7acc4348a8f9334f3c44927b` |
| `week9/__pycache__/test_expenses_given.cpython-314.pyc` | A — Generated Python bytecode; source/tests retained at root; safe to regenerate. | `dcaf1bf009cad1e2c4f0a4cbb1c039e7a633a2f795108d582ee5fef6138d3c0b` |
| `week9/diagram_review.md` | D — Retained as root diagram_review.md, with paths and instructions updated for the root implementation. | `6f8be256bd911018003aa436c54c7f73be917491b60a318432c395471247ac80` |
| `week9/expenses.py` | B — Corrected implementation reviewed and merged into root expenses.py, including all three improvements. | `664ff8d15d6ba15d867edfe074fe7a4412449a24c6714ad55dcd4ebc6b78e5ff` |
| `week9/research` | D — Copied byte-for-byte to root research.md. | `9b679c8438b4f305de88c8a277f5cd30594233681f223af9ca8b9bd1d471c34d` |
| `week9/test_expenses.py` | C — All 78 test methods migrated to root test_expenses.py; improvement test classes renamed without Week9 prefixes. | `98bd22bff86d45951cbbb17ab84b01431ed752184ccfc1b904c990204bc76ea7` |
| `week9/test_expenses_given.py` | F — Byte-identical to retained root test_expenses_given.py. | `b95a0520b5e2c0b944897bb486161a801b6934b161ec30cef8f1937cf3dc96e1` |
| `Lab Instructions/week5 (1).png` | A — Reference screenshot superseded by the extracted checklist. Functional decomposition and bottom-up implementation introduction; context retained in LAB_REVIEW.md. | `0e15291469e8d0eacde798f2dd9f20eb44b2311856ac2cd87c3733d29ff7592f` |
| `Lab Instructions/week5 (2).png` | A — Reference screenshot superseded by the extracted checklist. Purpose, prerequisites, demo, folder/commit instructions, original submission deadline and storage requirement extracted into LAB_REVIEW.md. | `b25b43f56dae836477c07a7d7aa6afd2cfc26fa90a9c2239d5d537ad067c0deb` |
| `Lab Instructions/week5 (3).png` | A — Reference screenshot superseded by the extracted checklist. CSV/startup/menu/input behaviour, single-file implementation, function size and repetition requirements extracted into LAB_REVIEW.md. | `733a98db6f20c84d42315e916c99063e457519c8b997f0ddc23ce6bf71e9e858` |
| `Lab Instructions/week5 (4).png` | A — Reference screenshot superseded by the extracted checklist. Prompt dictionary, unused artefacts, docstrings, main and original diagram/development process extracted into LAB_REVIEW.md. | `4ed71e8bfe4eaf3c56365cebc6975964a67be6c6779e0e83b65b3cd2547f797d` |
| `Lab Instructions/week5 (5).png` | A — Reference screenshot superseded by the extracted checklist. Learning-oriented commits, docstring-derived tests, Python comments and immutable lecturer regression extracted into LAB_REVIEW.md. | `51ae4412c53e3ddf2e64f84f609fd0478be84e6043cd3f40ac65a8c37b4ffc83` |
| `Lab Instructions/week5 (6).png` | A — Reference screenshot superseded by the extracted checklist. Final diagram similarity, matching numbers and bracketed function names retained in LAB_REVIEW.md and diagram_review.md. | `08ebffc77627a511310ea722278f8f316a7cf0c7b77fce1f3279b0a4d45eb004` |
| `Lab Instructions/week9 (1).png` | A — Reference screenshot superseded by the extracted checklist. Ethics introduction and example cases; background lecture context accounted for in LAB_REVIEW.md. | `1f476323ab65dda5acf9bf2882c795eb7205eabcce1064c766981d5d2c6c8a12` |
| `Lab Instructions/week9 (10).png` | A — Reference screenshot superseded by the extracted checklist. Copilot provenance and three improvements with affected people, prompts and summaries retained in README.md, research.md and LAB_REVIEW.md. | `5e7b46e5da10a9a3145a94c691916364f43b40cc43a83ee514d168ed1dda6690` |
| `Lab Instructions/week9 (2).png` | A — Reference screenshot superseded by the extracted checklist. Ethics and utilitarianism; background lecture context accounted for in LAB_REVIEW.md. | `7efdbe04e99c86c93cbd806d0a4a108bebe03795539d2a3b8c3a4fda89ade57a` |
| `Lab Instructions/week9 (3).png` | A — Reference screenshot superseded by the extracted checklist. Deontology and virtue ethics; background lecture context accounted for in LAB_REVIEW.md. | `09f1d0f6eadc1d0817f84f436e2379d9cb69cb75496ba16581710df695224890` |
| `Lab Instructions/week9 (4).png` | A — Reference screenshot superseded by the extracted checklist. AI ethics principles; background lecture context accounted for in LAB_REVIEW.md. | `3b07a03f501e64db36d658238f38c31c383aafff7afd19068350c9e66d6cfc2b` |
| `Lab Instructions/week9 (5).png` | A — Reference screenshot superseded by the extracted checklist. Sustainability, ownership and copyright background; corresponding research/provenance requirements retained in LAB_REVIEW.md. | `be51b63466a3443b1fb3c7ed701170a6c0738212ef21360b93d3bb3423518aa4` |
| `Lab Instructions/week9 (6).png` | A — Reference screenshot superseded by the extracted checklist. Ownership and academic integrity background; provenance and honest historical limits retained in LAB_REVIEW.md. | `088e04eccc4d1ea61457ee1f517341b72317f173afd234eb443ba6e0bf52a33e` |
| `Lab Instructions/week9 (7).png` | A — Reference screenshot superseded by the extracted checklist. Common genAI mistakes; background supporting the documented independent tests and review. | `9586e43ebe823189074e1b01f17b144b4ab509fe94d208f6eed3f22d39d68989` |
| `Lab Instructions/week9 (8).png` | A — Reference screenshot superseded by the extracted checklist. Module responsibilities for users, developers, privacy and attribution; corresponding checklist retained in LAB_REVIEW.md. | `641e6e03e3d8525e9aa9279bb4efbb98609bd4ebb55c49d4ec4ccaf12ada8b13` |
| `Lab Instructions/week9 (9).png` | A — Reference screenshot superseded by the extracted checklist. Research/privacy questions, prerequisites, demo and commit instructions extracted into LAB_REVIEW.md; answers retained in research.md. | `c27adb0ed34b54e019f04819b7626ad29c6ef21432859df9fbc901d4c55a2239` |

Protected root material, unchanged during consolidation:

| File | SHA-256 |
| --- | --- |
| `test_expenses_given.py` | `b95a0520b5e2c0b944897bb486161a801b6934b161ec30cef8f1937cf3dc96e1` |
| `expenses.csv` | `3260f4047854853aa09975c20270f5ab56c4cbb316a7a8812bbb772791ef46ea` |
| `expensediagram.jpg` | `1ad2e08e2f160f1e2a161213a470f4565d71e2dd23957904268431b97ec18cbf` |
| `expensediagramfinal.jpg` | `34120ff7ef0a1599f48c2a4626239c49acbad76a5c087d876d9121a4ace9e2c0` |
| `before/test_expenses_original.py.txt` | `74607fc023da40ae6e77454231cfe3a85c0fde64637137cd8f1e88da3a65cf77` |

