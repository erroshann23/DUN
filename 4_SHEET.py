#========================================================
# DUN CUTTING PLAN
# INPUT DATA
# PROJECT INFORMATION
Name = "Darlipalli"              # Project / Customer name
SO = "SO12121232131"             # Sale Order number
BktType = "Type_B"               # Type of the Basket
DNo = "D-13-54-00542"            # Drawing Number
# Coil Details
cw = 305                         # Coil width (mm)
ct = 1.2                         # Coil thickness (mm)
# Profile Details
hu = 3.7                        # Undulation height (mm)
hn = 9.8                         # Notch height (mm)
p = 71.7                         # Notch pitch (mm)
wn = 18.0                        # Notch width (mm)
# Basket Dimensions
qty = 4                          # Basket quantity
lbo = 512.8                        # Bottom outer length (mm)
lto = 671.5                        # Top outer length (mm)
ho = 911.2                         # Outer height (mm)
tbf = 3.15                          # Basket frame thickness (mm)
tf = 6                           # Filling tolerance (mm)
web = 51.58                      # Empty Basket weight (kg)
wmin = 250.48                    # Engg Minimum Basket weight (kg)
wmax = 263.66                    # Engg Maximum Basket weight (kg)
# Sheet Matching Tolerance
tol = 2                          # Allowable SHM tolerance (mm)
# Single Sheet Condition
group_size = 10                  # Size of a Group During Single Sheet Plan
# HEAL Condition
max_shear_length = 2400          # Critical Length for HEAL Cutting

# CALCULATE PARAMETERS
def calculate_parameters():
    hp = hu + hn                          # Pair Height
    lb = lbo - 2 * tbf - tf               # Bottom Length
    lt = lto - 2 * tbf - tf               # Top Length
    h = ho - 2 * tbf - 3                  # Height
    incr = (lt - lb) / h                  # Tanθ (Increment)
    shq = round(h / hp * 2)               # Sheet Quantity
    wnc = wn + 0.0092857 * cw + 0.7142857 # Corrected Notch Width
    return {"hp": hp,
        "lb": lb,
        "lt": lt,
        "h": h,
        "incr": incr,
        "shq": shq,
        "wnc": wnc,
        "p": p,
        "tol": tol,
        "max_shear_length": max_shear_length,
        "qty": qty,
        "group_size": group_size,}

# DISPLAY INPUTS AND CALCULATED PARAMETERS
def display_inputs(params):
    print("=" * 60)
    print("                 DUN CUTTING PLAN")
    print("=" * 60)
    print("\n---------------- PROJECT DATA ----------------")
    print("Project Name           :", Name)
    print("SO Number              :", SO)
    print("Basket Type            :", BktType)
    print("Drawing Number         :", DNo)
    print("\n---------------- COIL DETAILS ----------------")
    print("Coil Width             :", cw, "mm")
    print("Coil Thickness         :", ct, "mm")
    print("\n---------------- PROFILE DETAILS -------------")
    print("Undulation Height      :", hu, "mm")
    print("Notch Height           :", hn, "mm")
    print("Notch Pitch            :", p, "mm")
    print("Notch Width            :", wn, "mm")
    print("\n-------------- BASKET DETAILS ---------------")
    print("Basket Quantity        :", qty)
    print("Bottom Outer Length    :", lbo, "mm")
    print("Top Outer Length       :", lto, "mm")
    print("Outer Height           :", ho, "mm")
    print("Frame Thickness        :", tbf, "mm")
    print("Filling Tolerance      :", tf, "mm")
    print("\n--------------- HEAL CONDITIONS --------------")
    print("Critical HEAL Length   :", max_shear_length, "mm")
    print("\n-------- SINGLE SHEET GROUP DETAILS ----------")
    print("Single Sheet Group QTY :", group_size, "Nos")
    print("\n------------ CALCULATED PARAMETERS -----------")
    print("Pair Height            :", round(params["hp"], 2), "mm")
    print("Bottom Length          :", round(params["lb"], 2), "mm")
    print("Top Length             :", round(params["lt"], 2), "mm")
    print("Height                 :", round(params["h"], 2), "mm")
    print("Tanθ (Increment)       :", round(params["incr"], 2))
    print("Sheet Quantity         :", params["shq"], "Nos")
    print("Corrected Notch W.     :", round(params["wnc"], 1), "mm")
    print("Empty Basket Weight    :", web, "kg")
    print("Minimum Basket Weight  :", wmin, "kg")
    print("Maximum Basket Weight  :", wmax, "kg")
    print("Matching Tolerance     :", tol, "mm")

# GENERATE SHEETS
def generate_sheets(params):
    odd_sheets = []
    even_sheets = []

    for i in range(1, params["shq"] + 1):
        shloc = hn / 2 + (i - 1) * params["hp"] / 2
        shl = params["lb"] + shloc * params["incr"]
        sheet = (i, shloc, shl)
        if i % 2 == 0:
            even_sheets.append(sheet)
        else:
            odd_sheets.append(sheet)

    return odd_sheets, even_sheets


def create_single_sheet_groups(all_sheets, group_size):
    all_sheets = sorted(all_sheets, key=lambda x: x[0])
    groups = [all_sheets[i:i + group_size]
        for i in range(0, len(all_sheets), group_size)]

    if len(groups) > 1 and len(groups[-1]) < 3:
        groups[-2].extend(groups.pop())
    return groups

# DISPLAY GENERATED SHEETS
def display_sheets(odd_sheets, even_sheets):
    print("\n" + "-" * 25 + " ODD SHEETS " + "-" * 25 + "    " + "-" * 25 + " EVEN SHEETS " + "-" * 24)
    print(f"{'Sheet No.':>15} " f"{'Location (mm)':>21} " f"{'Length (mm)':>20} "
          f"    " f"{'Sheet No.':>15} " f"{'Location (mm)':>21} " f"{'Length (mm)':>20}")
    print("-" * 62 + "    " + "-" * 62)

    max_rows = max(len(odd_sheets), len(even_sheets))

    for i in range(max_rows):
        if i < len(odd_sheets):
            no, loc, length = odd_sheets[i]
            odd_text = f"{no:>10} {loc:>21.2f} {length:>20.0f}"
        else:
            odd_text = f"{'':>10} {'':>21} {'':>20}"

        if i < len(even_sheets):
            no, loc, length = even_sheets[i]
            even_text = f"{no:>15} {loc:>21.2f} {length:>20.0f}"
        else:
            even_text = f"{'':>15} {'':>21} {'':>20}"
        print(odd_text + "    " + even_text)

# GET UNMATCHED SHEETS
def get_unmatched_sheets(all_sheets, matched_sheets):
    matched_numbers = {sheet[0] for sheet in matched_sheets}
    return [sheet for sheet in all_sheets
        if sheet[0] not in matched_numbers]

# GET MATCHED SHEETS
def get_match_range(all_sheets, reference_no, match_no, reverse):
    if reverse:
        return [sheet for sheet in all_sheets
            if match_no <= sheet[0] <= reference_no]

    return [sheet for sheet in all_sheets
        if reference_no <= sheet[0] <= match_no]

# CALCULATE SHM / C
def calculate_match_value(reference_length, sheet_length, odd_even, same_direction, wnc):
    if same_direction: #Same Direction
        if odd_even: 
            return reference_length % p #C Value for Odd-Even & Even-Odd Sheets
        return p - (reference_length % p) #C Value for Odd-Odd & Even-Even Sheets

    if odd_even: #Opposite Direction
        return p - ((reference_length + sheet_length - wnc - p / 2) % p) #C Value for Odd-Even & Even-Odd Sheets
    return p - ((reference_length + sheet_length - wnc) % p) #C Value for Odd-Odd & Even-Even Sheets

# CALCULATE C FOR EACH PAIR
def calculate_pair_c_value(sh1_length, sh2_length, odd_even, same_direction, p, wnc, tol):
    if same_direction: #Same Direction
        if odd_even:
            shm = sh2_length % p #C Value for Odd-Even & Even-Odd Sheets
        else:
            shm = p - (sh2_length % p) #C Value for Odd-Odd & Even-Even Sheets
    else: #Opposite Direction
        if odd_even:
            shm = p - ((sh1_length + sh2_length - wnc - p / 2) % p) #C Value for Odd-Even & Even-Odd Sheets
        else:
            shm = p - ((sh1_length + sh2_length - wnc) % p) #C Value for Odd-Odd & Even-Even Sheets

    if shm <= tol or (p - shm) <= tol:
        return 0
    return round(shm, 0)

# HEAL SHEARING LENGTH CALCULATION
def calculate_shear_length(sh1_length, sh2_length, c_value):
    return sh1_length + sh2_length + 70 + c_value

def check_single_sheet_limit(groups, max_shear_length):
    for group in groups:
        max_sheet_length = max(sheet[2] for sheet in group)
        if max_sheet_length + 70 > max_shear_length:
            return False
    return True

def check_two_sheet_shear_limit(matched_table, max_shear_length):
    return any(row["shear_length"] > max_shear_length
        for row in matched_table)

def calculate_single_sheet_heal(groups):
    table = []

    for group_number, group in enumerate(groups, start=1):
        max_sheet = max(group, key=lambda x: x[2])
        heal_length = max_sheet[2] + 70

        for sheet in group:
            table.append({
                "group": group_number,
                "sh_no": sheet[0],
                "sh1_length": sheet[2],
                "heal_length": heal_length,
            })

        if group_number < len(groups):
            table.append(None)

    return table

# CREATE MATCHED PAIRS
def create_matched_pairs(matched_sheets, method):
    if not matched_sheets:
        return []

    is_odd_even = (
        "Odd-Even" in method or "Even-Odd" in method
    )

    if is_odd_even:
        odd_sheets = sorted(
            [sheet for sheet in matched_sheets if sheet[0] % 2 != 0],
            key=lambda x: x[0],
        )
        even_sheets = sorted(
            [sheet for sheet in matched_sheets if sheet[0] % 2 == 0],
            key=lambda x: x[0],
        )

        if not odd_sheets or not even_sheets:
            return []

        largest_sheet = max(matched_sheets, key=lambda x: x[0])

        if largest_sheet[0] % 2 != 0:
            sh1_group = list(reversed(odd_sheets))
            sh2_group = even_sheets
        else:
            sh1_group = list(reversed(even_sheets))
            sh2_group = odd_sheets

        return list(zip(sh1_group, sh2_group))

    matched_sheets = sorted(matched_sheets, key=lambda x: x[0])
    total = len(matched_sheets)

    if total % 2 == 0:
        half = total // 2
        sh1_group = matched_sheets[:half]
        sh2_group = list(reversed(matched_sheets[half:]))
        return list(zip(sh1_group, sh2_group))

    half = total // 2
    sh1_group = matched_sheets[:half]
    middle_sheet = matched_sheets[half]
    sh2_group = list(reversed(matched_sheets[half + 1:]))

    matched_pairs = list(zip(sh1_group, sh2_group))
    matched_pairs.append((middle_sheet, middle_sheet))
    return matched_pairs

def display_single_sheet_heal(table):
    print("\n" + "=" * 65)
    print("SINGLE SHEET HEAL CUTTING CALCULATION")
    print("=" * 65)
    print(
        f"{'SH No.':>10}"
        f"{'SH1 Length (mm)':>22}"
        f"{'HEAL Length (mm)':>22}"
    )
    print("-" * 65)

    for row in table:
        if row is None:
            print()
            continue

        print(
            f"{row['sh_no']:>10}"
            f"{row['sh1_length']:>22.0f}"
            f"{row['heal_length']:>22.0f}"
        )

    print("=" * 65)


def run_single_sheet_plan(odd_sheets, even_sheets, params):
    all_sheets = sorted(odd_sheets + even_sheets, key=lambda x: x[0])
    groups = create_single_sheet_groups(all_sheets, params["group_size"])
    group_results = calculate_single_sheet_heal(groups)
    display_single_sheet_heal(group_results)

    limit_ok = check_single_sheet_limit(
        groups, params["max_shear_length"]
    )

    print("\nMaximum Machine Shearing Length :",
          params["max_shear_length"], "mm")
    print("\nSingle Sheet HEAL Limit Check")
    print("-" * 60)

    if limit_ok:
        print("RESULT : All single-sheet groups are within")
        print("        the machine shearing limit.")
    else:
        print("RESULT : WARNING - A single-sheet group also")
        print("        exceeds the machine shearing limit.")

    return group_results

# GET METHOD NAME
def get_method_name(reference_group, candidate_group, reverse,
                    same_direction):
    reference_parity = (
        "Odd" if reference_group[0][0] % 2 != 0 else "Even"
    )
    candidate_parity = (
        "Odd" if candidate_group[0][0] % 2 != 0 else "Even"
    )
    direction = "Last → First" if reverse else "First → Last"

    if same_direction:
        return (
            f"Same Direction {reference_parity}-{candidate_parity} "
            f"{direction}"
        )

    return f"{reference_parity}-{candidate_parity} {direction}"

# MATCH SHEETS
def match_sheets(reference_group, candidate_group, current_sheets,
                 reverse, odd_even, same_direction, stage, wnc,
                 residual=False):
    if not reference_group or not candidate_group:
        return {
            "best_match": None,
            "shm": None,
            "c": None,
            "matched": 0,
            "unmatched": len(current_sheets),
            "unmatched_percentage": 100,
            "matched_sheets": [],
            "no_match": True,
        }

    reference_sheet = (
        reference_group[-1] if reverse else reference_group[0]
    )
    reference_no = reference_sheet[0]
    reference_length = reference_sheet[2]
    valid_matches = []

    for sheet in candidate_group:
        sheet_no = sheet[0]
        sheet_length = sheet[2]

        if not reverse and sheet_no < reference_no:
            continue
        if reverse and sheet_no > reference_no:
            continue

        value = calculate_match_value(
            reference_length, sheet_length, odd_even,
            same_direction, wnc
        )
        shm = value
        c = value

        if stage == 1 and not residual:
            if shm <= tol or (p - shm) <= tol:
                valid_matches.append((sheet_no, shm, c))
        else:
            valid_matches.append((sheet_no, shm, c))

    if not valid_matches:
        return {
            "method": get_method_name(
                reference_group, candidate_group, reverse,
                same_direction
            ),
            "reference_no": reference_no,
            "best_match": None,
            "shm": None,
            "c": None,
            "matched": 0,
            "unmatched": len(current_sheets),
            "unmatched_percentage": 100,
            "matched_sheets": [],
            "no_match": True,
        }

    if same_direction:
        best = min(valid_matches, key=lambda x: x[2])
    elif reverse:
        best = min(valid_matches, key=lambda x: x[0])
    else:
        best = max(valid_matches, key=lambda x: x[0])

    match_no, match_shm, match_c = best
    matched_sheets = get_match_range(
        current_sheets, reference_no, match_no, reverse
    )
    matched = len(matched_sheets)
    total = len(current_sheets)
    unmatched = total - matched
    unmatched_percentage = (
        (unmatched / total) * 100 if total > 0 else 0
    )

    return {
        "method": get_method_name(
            reference_group, candidate_group, reverse, same_direction
        ),
        "reference_no": reference_no,
        "best_match": match_no,
        "shm": match_shm,
        "c": match_c,
        "matched": matched,
        "unmatched": unmatched,
        "unmatched_percentage": unmatched_percentage,
        "matched_sheets": matched_sheets,
        "no_match": False,
    }

# BUILD NORMAL MATCHING RESULTS
def build_normal_results(current_sheets, stage, wnc):
    odd_sheets = [
        sheet for sheet in current_sheets if sheet[0] % 2 != 0
    ]
    even_sheets = [
        sheet for sheet in current_sheets if sheet[0] % 2 == 0
    ]
    results = {}

    if odd_sheets:
        results["Odd-Odd First → Last"] = match_sheets(
            odd_sheets, odd_sheets, current_sheets,
            False, False, False, stage, wnc
        )
        results["Odd-Odd Last → First"] = match_sheets(
            odd_sheets, odd_sheets, current_sheets,
            True, False, False, stage, wnc
        )

    if odd_sheets and even_sheets:
        results["Odd-Even First → Last"] = match_sheets(
            odd_sheets, even_sheets, current_sheets,
            False, True, False, stage, wnc
        )
        results["Odd-Even Last → First"] = match_sheets(
            odd_sheets, even_sheets, current_sheets,
            True, True, False, stage, wnc
        )
        results["Even-Odd First → Last"] = match_sheets(
            even_sheets, odd_sheets, current_sheets,
            False, True, False, stage, wnc
        )
        results["Even-Odd Last → First"] = match_sheets(
            even_sheets, odd_sheets, current_sheets,
            True, True, False, stage, wnc
        )

    if even_sheets:
        results["Even-Even First → Last"] = match_sheets(
            even_sheets, even_sheets, current_sheets,
            False, False, False, stage, wnc
        )
        results["Even-Even Last → First"] = match_sheets(
            even_sheets, even_sheets, current_sheets,
            True, False, False, stage, wnc
        )

    if stage >= 2:
        if odd_sheets:
            results["Same Direction Odd-Odd First → Last"] = match_sheets(
                odd_sheets, odd_sheets, current_sheets,
                False, False, True, stage, wnc
            )
            results["Same Direction Odd-Odd Last → First"] = match_sheets(
                odd_sheets, odd_sheets, current_sheets,
                True, False, True, stage, wnc
            )

        if odd_sheets and even_sheets:
            results["Same Direction Odd-Even First → Last"] = match_sheets(
                odd_sheets, even_sheets, current_sheets,
                False, True, True, stage, wnc
            )
            results["Same Direction Odd-Even Last → First"] = match_sheets(
                odd_sheets, even_sheets, current_sheets,
                True, True, True, stage, wnc
            )
            results["Same Direction Even-Odd First → Last"] = match_sheets(
                even_sheets, odd_sheets, current_sheets,
                False, True, True, stage, wnc
            )
            results["Same Direction Even-Odd Last → First"] = match_sheets(
                even_sheets, odd_sheets, current_sheets,
                True, True, True, stage, wnc
            )

        if even_sheets:
            results["Same Direction Even-Even First → Last"] = match_sheets(
                even_sheets, even_sheets, current_sheets,
                False, False, True, stage, wnc
            )
            results["Same Direction Even-Even Last → First"] = match_sheets(
                even_sheets, even_sheets, current_sheets,
                True, False, True, stage, wnc
            )

    return results

# SELECT NORMAL MATCHING METHOD
def select_normal_method(results, stage):
    valid_results = {
        method: result for method, result in results.items()
        if not result["no_match"]
    }

    if not valid_results:
        return None

    if stage == 1:
        return min(
            valid_results.items(),
            key=lambda x: x[1]["unmatched_percentage"]
        )

    opposite_c_limit = p * 0.35
    same_c_limit = 20
    allowable_methods = {}

    for method, result in valid_results.items():
        c = result["c"]

        if "Same Direction" in method:
            if c < same_c_limit:
                allowable_methods[method] = result
        elif c <= opposite_c_limit:
            allowable_methods[method] = result

    if not allowable_methods:
        return None

    return min(
        allowable_methods.items(),
        key=lambda x: (
            x[1]["unmatched_percentage"],
            x[1]["c"]
        )
    )

# FINAL RESIDUAL - GENERATE ALL POSSIBLE OPTIONS
def get_residual_options(current_sheets, wnc):
    current_sheets = sorted(current_sheets, key=lambda x: x[0])

    odd_sheets = [
        sheet for sheet in current_sheets if sheet[0] % 2 != 0
    ]
    even_sheets = [
        sheet for sheet in current_sheets if sheet[0] % 2 == 0
    ]

    groups = [
        ("Odd-Odd", odd_sheets, odd_sheets, False),
        ("Odd-Even", odd_sheets, even_sheets, True),
        ("Even-Odd", even_sheets, odd_sheets, True),
        ("Even-Even", even_sheets, even_sheets, False),
    ]
    options = []

    for pair_name, reference_group, candidate_group, odd_even in groups:
        if not reference_group or not candidate_group:
            continue

        for reverse in (False, True):
            reference_sheet = (
                reference_group[-1] if reverse else reference_group[0]
            )
            reference_no = reference_sheet[0]
            reference_length = reference_sheet[2]

            for candidate in candidate_group:
                candidate_no = candidate[0]
                candidate_length = candidate[2]

                if not reverse and candidate_no < reference_no:
                    continue
                if reverse and candidate_no > reference_no:
                    continue

                matched_sheets = get_match_range(
                    current_sheets, reference_no, candidate_no, reverse
                )
                if not matched_sheets:
                    continue

                remaining_sheets = get_unmatched_sheets(
                    current_sheets, matched_sheets
                )
                direction = (
                    "Last → First" if reverse else "First → Last"
                )

                # Opposite-direction matching
                c = calculate_match_value(
                    reference_length, candidate_length,
                    odd_even, False, wnc
                )
                options.append({
                    "method": f"{pair_name} {direction}",
                    "reference_no": reference_no,
                    "best_match": candidate_no,
                    "shm": c,
                    "c": c,
                    "matched": len(matched_sheets),
                    "unmatched": len(remaining_sheets),
                    "matched_sheets": matched_sheets,
                    "remaining_sheets": remaining_sheets,
                })

                # Same-direction matching
                c = calculate_match_value(
                    reference_length, candidate_length,
                    odd_even, True, wnc
                )
                options.append({
                    "method": f"Same Direction {pair_name} {direction}",
                    "reference_no": reference_no,
                    "best_match": candidate_no,
                    "shm": c,
                    "c": c,
                    "matched": len(matched_sheets),
                    "unmatched": len(remaining_sheets),
                    "matched_sheets": matched_sheets,
                    "remaining_sheets": remaining_sheets,
                })

    return options

# FINAL RESIDUAL - FIND COMPLETE SOLUTION
def find_best_residual(current_sheets, wnc):
    if not current_sheets:
        return (0, 0, 0, [])

    best_solution = None
    options = get_residual_options(current_sheets, wnc)

    for option in options:
        remaining = option["remaining_sheets"]

        if len(remaining) >= len(current_sheets):
            continue

        next_solution = find_best_residual(remaining, wnc)
        if next_solution is None:
            continue

        total_c = option["c"] + next_solution[0]
        maximum_c = max(option["c"], next_solution[1])
        stages = 1 + next_solution[2]
        path = [option] + next_solution[3]
        solution = (total_c, maximum_c, stages, path)

        if best_solution is None:
            best_solution = solution
        else:
            current_score = solution[:3]
            best_score = best_solution[:3]

            if current_score < best_score:
                best_solution = solution

    return best_solution

# DISPLAY NORMAL COMPARISON
def display_comparison(results, stage):
    print("\n" + "=" * 60)
    print("             UNMATCHED SHEETS COMPARISON")
    print("=" * 60)

    for method, result in results.items():
        if stage == 1:
            print(
                f"{method:<45} : "
                f"{result['unmatched_percentage']:.2f} % unmatched"
            )
        else:
            c = result["c"]
            c_text = "No Match" if c is None else f"{c:.2f} mm"
            print(
                f"{method:<50} : "
                f"{result['unmatched_percentage']:.2f} % unmatched"
                f" | C = {c_text}"
            )

# DISPLAY BEST NORMAL RESULT
def display_best_result(stage, result):
    print("\n" + "=" * 60)
    print(f"             BEST MATCHING - STAGE {stage}")
    print("=" * 60)
    print("Matching Method     :", result["method"])
    print("Reference Sheet     :", result["reference_no"])
    print("Best Match Sheet    :", result["best_match"])
    print("SHM                 :", f"{result['shm']:.2f} mm")
    print("C                   :", f"{result['c']:.2f} mm")
    print("Matched Sheets      :", result["matched"])
    print("Unmatched Sheets    :", result["unmatched"])
    print("Unmatched Percentage:", f"{result['unmatched_percentage']:.2f} %")
    print("Matched Sheet Nos.  :", [
        sheet[0] for sheet in result["matched_sheets"]
    ])

# DISPLAY FINAL RESIDUAL RESULT
def display_residual_result(solution):
    total_c, maximum_c, stages, path = solution

    print("\n" + "=" * 60)
    print("             FINAL RESIDUAL MATCHING")
    print("=" * 60)
    print("Residual Stages     :", stages)
    print("Total C             :", f"{total_c:.2f} mm")
    print("Maximum C           :", f"{maximum_c:.2f} mm")

    for i, result in enumerate(path, start=1):
        print("\n" + "-" * 60)
        print(f"FINAL RESIDUAL STAGE {i}")
        print("-" * 60)
        print("Matching Method     :", result["method"])
        print("Reference Sheet     :", result["reference_no"])
        print("Best Match Sheet    :", result["best_match"])
        print("SHM                 :", f"{result['shm']:.2f} mm")
        print("C                   :", f"{result['c']:.2f} mm")
        print("Matched Sheets      :", result["matched"])
        print("Matched Sheet Nos.  :", [
            sheet[0] for sheet in result["matched_sheets"]
        ])
        print("Remaining Sheet Nos.:", [
            sheet[0] for sheet in result["remaining_sheets"]
        ])


def create_matched_sheet_table(matched_pairs, method, p, wnc, tol):
    same_direction = "Same Direction" in method
    odd_even = "Odd-Even" in method or "Even-Odd" in method
    table = []

    for sh1, sh2 in matched_pairs:
        sh1_no, sh1_length = sh1[0], sh1[2]
        sh2_no, sh2_length = sh2[0], sh2[2]

        c_value = calculate_pair_c_value(
            sh1_length, sh2_length, odd_even,
            same_direction, p, wnc, tol
        )
        shear_length = calculate_shear_length(
            sh1_length, sh2_length, c_value
        )

        table.append({
            "sh1_no": sh1_no,
            "sh1_length": sh1_length,
            "sh2_no": sh2_no,
            "sh2_length": sh2_length,
            "shear_length": shear_length,
            "c_value": c_value,
        })

    return table

# ============================================================
# COLLECT FINAL HEAL TABLE RESULTS
# ============================================================

def collect_heal_results(
    four_sheet_groups,
    two_sheet_table,
    stage,
    three_sheet_groups=None):
    results = []

    # FOUR-SHEET RESULTS -------------------------------------
    for group in four_sheet_groups:
        results.append({
            "stage": stage,
            "scheme": 4,
            "sh1_no": group["sh1_no"],
            "sh1_length": group["sh1_length"],
            "sh2_no": group["sh2_no"],
            "sh2_length": group["sh2_length"],
            "sh3_no": group["sh3_no"],
            "sh3_length": group["sh3_length"],
            "sh4_no": group["sh4_no"],
            "sh4_length": group["sh4_length"],
            "c_value": group["c_value"],
            "g_value": group["g_value"],
            "heal_length": group["heal_length"]
        })

    # THREE-SHEET RESULTS ------------------------------------
    if three_sheet_groups is None:
        three_sheet_groups = []

    for group in three_sheet_groups:
        results.append({
            "stage": stage,
            "scheme": 3,
            "sh1_no": group["sh1_no"],
            "sh1_length": group["sh1_length"],
            "sh2_no": group["sh2_no"],
            "sh2_length": group["sh2_length"],
            "sh3_no": group["sh3_no"],
            "sh3_length": group["sh3_length"],
            "sh4_no": None,
            "sh4_length": None,
            "c_value": group["c_value"],
            "g_value": None,
            "heal_length": group["heal_length"]
        })

    # TWO-SHEET RESULTS --------------------------------------
    for pair in two_sheet_table:
        results.append({
            "stage": stage,
            "scheme": 2,
            "sh1_no": pair["sh1_no"],
            "sh1_length": pair["sh1_length"],
            "sh2_no": pair["sh2_no"],
            "sh2_length": pair["sh2_length"],
            "sh3_no": None,
            "sh3_length": None,
            "sh4_no": None,
            "sh4_length": None,
            "c_value": pair["c_value"],
            "g_value": None,
            "heal_length": pair["shear_length"]
        })

    return results

# DISPLAY FINAL HEAL CALCULATION TABLE
def display_final_heal_table(all_results):
    if not all_results:
        print("\nNo HEAL matching results available.")
        return

    schemes_used = {row["scheme"] for row in all_results}
    max_scheme = max(schemes_used)

    print("\n" + "=" * 120)
    print("                       FINAL HEAL CUTTING CALCULATION TABLE")
    print("=" * 120)

    if max_scheme == 2:
        print(
            f"{'SH1 No.':>9}{'SH1 Length':>13}"
            f"{'SH2 No.':>9}{'SH2 Length':>13}"
            f"{'HEAL Length':>15}{'C':>10}"
        )
        print("-" * 69)
        previous_stage = None

        for row in all_results:
            current_stage = row["stage"]
            if previous_stage is not None and current_stage != previous_stage:
                print()

            print(
                f"{row['sh1_no']:>9}"
                f"{row['sh1_length']:>13.0f}"
                f"{row['sh2_no']:>9}"
                f"{row['sh2_length']:>13.0f}"
                f"{row['heal_length']:>15.0f}"
                f"{row['c_value']:>10.0f}"
            )
            previous_stage = current_stage

    else:
        print(
            f"{'SH1 No.':>9}{'SH1 Length':>13}"
            f"{'SH2 No.':>9}{'SH2 Length':>13}"
            f"{'SH3 No.':>9}{'SH3 Length':>13}"
            f"{'SH4 No.':>9}{'SH4 Length':>13}"
            f"{'C':>8}{'G':>8}{'HEAL Length':>14}"
        )
        print("-" * 120)

        def display_value(value, width, decimals=False):
            if value is None:
                return f"{'':>{width}}"
            if decimals:
                return f"{value:>{width}.0f}"
            return f"{value:>{width}}"

        previous_stage = None

        for row in all_results:
            current_stage = row["stage"]
            if previous_stage is not None and current_stage != previous_stage:
                print()

            print(
                display_value(row["sh1_no"], 9)
                + display_value(row["sh1_length"], 13, True)
                + display_value(row["sh2_no"], 9)
                + display_value(row["sh2_length"], 13, True)
                + display_value(row["sh3_no"], 9)
                + display_value(row["sh3_length"], 13, True)
                + display_value(row["sh4_no"], 9)
                + display_value(row["sh4_length"], 13, True)
                + display_value(row["c_value"], 8, True)
                + display_value(row["g_value"], 8, True)
                + display_value(row["heal_length"], 14, True)
            )
            previous_stage = current_stage

# COMBINE OPPOSITE-DIRECTION PAIRS INTO 4-SHEET GROUPS
def combine_four_sheet_pairs(pair_table, max_shear_length, qty):
    threshold = int((max_shear_length - 95) / 2)
    eligible_pairs = []
    remaining_pairs = []

    for pair in pair_table:
        if int(pair["shear_length"] - 70) <= threshold:
            eligible_pairs.append(pair)
        else:
            remaining_pairs.append(pair)

    four_sheet_groups = []
    used_pairs = set()

    for i, pair_a in enumerate(eligible_pairs):
        if i in used_pairs:
            continue

        for j, pair_b in enumerate(eligible_pairs):
            if j == i or j in used_pairs:
                continue

            a1, a2 = pair_a["sh1_no"], pair_a["sh2_no"]
            b1, b2 = pair_b["sh1_no"], pair_b["sh2_no"]

            a_repeated = a1 == a2
            b_repeated = b1 == b2
            all_same = a1 == a2 == b1 == b2
            corresponding_pairs_equal = a1 == b1 and a2 == b2

            # Reject when only one pair repeats its sheet number.
            if a_repeated != b_repeated:
                continue

            # Special case 1: all four sheet references are identical.
            # The basket quantity must be divisible by four.
            if all_same:
                if qty % 4 != 0:
                    continue

            # Special case 2: both pairs repeat internally, but refer to
            # two different sheet numbers. Basket quantity must be even.
            elif a_repeated and b_repeated:
                if qty % 2 != 0:
                    continue

            # Special case 3: corresponding positions match across pairs,
            # while each pair contains two different sheet numbers.
            elif corresponding_pairs_equal:
                if qty % 2 != 0:
                    continue

            else:
                # Normal four-sheet matching requires four unique sheets.
                sheet_numbers = [a1, a2, b1, b2]
                if len(set(sheet_numbers)) != 4:
                    continue

            # Preserve the original parity rule for all cases except the
            # all-identical case, where parity cannot differ by definition.
            if not all_same and a2 % 2 == b1 % 2:
                continue

            sh1_length = pair_a["sh1_length"]
            sh2_length = pair_a["sh2_length"]
            sh3_length = pair_b["sh1_length"]
            sh4_length = pair_b["sh2_length"]

            c_value = pair_a["c_value"]
            g_value = pair_b["c_value"]

            heal_length = (
                sh1_length + sh2_length + sh3_length + sh4_length
                + 70 + 25 + c_value + g_value
            )

            if heal_length > max_shear_length:
                continue

            four_sheet_groups.append({
                "sh1_no": a1,
                "sh1_length": sh1_length,
                "sh2_no": a2,
                "sh2_length": sh2_length,
                "sh3_no": b1,
                "sh3_length": sh3_length,
                "sh4_no": b2,
                "sh4_length": sh4_length,
                "c_value": c_value,
                "g_value": g_value,
                "heal_length": heal_length,
            })

            used_pairs.add(i)
            used_pairs.add(j)
            break

    for i, pair in enumerate(eligible_pairs):
        if i not in used_pairs:
            remaining_pairs.append(pair)

    return four_sheet_groups, remaining_pairs

# STAGE 2: COMBINE STAGE 1 C=0 LEFTOVER PAIRS WITH STAGE 2 PAIRS
# The Stage 1 pair must have C=0. The Stage 2 candidate may have C=0 or
# an allowable C up to the existing Stage 2 limit (P * 0.35).
def combine_stage2_four_sheet_pairs(
    stage1_pairs, stage2_pairs, max_shear_length, qty, c_limit
):
    four_sheet_groups = []
    used_stage1 = set()
    used_stage2 = set()
    threshold = int((max_shear_length - 95) / 2)

    for i, pair_a in enumerate(stage1_pairs):
        a1, a2 = pair_a["sh1_no"], pair_a["sh2_no"]

        # Stage 1 leftover pair must be distinct-sheet and C=0.
        if a1 == a2 or abs(float(pair_a["c_value"])) > 1e-9:
            continue
        if int(pair_a["shear_length"] - 70) > threshold:
            continue

        for j, pair_b in enumerate(stage2_pairs):
            if j in used_stage2:
                continue

            candidate_c = float(pair_b["c_value"])
            if candidate_c < 0 or candidate_c > c_limit:
                continue
            if int(pair_b["shear_length"] - 70) > threshold:
                continue

            b1, b2 = pair_b["sh1_no"], pair_b["sh2_no"]
            a_repeated = a1 == a2
            b_repeated = b1 == b2
            all_same = a1 == a2 == b1 == b2
            corresponding_pairs_equal = a1 == b1 and a2 == b2

            # Keep the existing four-sheet repeated-number/QTY rules.
            if a_repeated != b_repeated:
                continue
            if all_same:
                if qty % 4 != 0:
                    continue
            elif a_repeated and b_repeated:
                if qty % 2 != 0:
                    continue
            elif corresponding_pairs_equal:
                if qty % 2 != 0:
                    continue
            elif len({a1, a2, b1, b2}) != 4:
                continue

            # Only the four specified opposite-direction sequences are allowed.
            sequence = tuple(
                "O" if number % 2 else "E"
                for number in (a1, a2, b1, b2)
            )
            if sequence not in {
                ("O", "O", "E", "E"),
                ("E", "E", "O", "O"),
                ("O", "E", "O", "E"),
                ("E", "O", "E", "O"),
            }:
                continue

            sh1_length = pair_a["sh1_length"]
            sh2_length = pair_a["sh2_length"]
            sh3_length = pair_b["sh1_length"]
            sh4_length = pair_b["sh2_length"]
            c_value = float(pair_a["c_value"])
            g_value = candidate_c

            heal_length = (
                sh1_length + sh2_length + sh3_length + sh4_length
                + 70 + 25 + c_value + g_value
            )
            if heal_length > max_shear_length:
                continue

            four_sheet_groups.append({
                "sh1_no": a1,
                "sh1_length": sh1_length,
                "sh2_no": a2,
                "sh2_length": sh2_length,
                "sh3_no": b1,
                "sh3_length": sh3_length,
                "sh4_no": b2,
                "sh4_length": sh4_length,
                "c_value": c_value,
                "g_value": g_value,
                "heal_length": heal_length,
            })
            used_stage1.add(i)
            used_stage2.add(j)
            break

    remaining_stage1 = [
        pair for i, pair in enumerate(stage1_pairs) if i not in used_stage1
    ]
    remaining_stage2 = [
        pair for j, pair in enumerate(stage2_pairs) if j not in used_stage2
    ]
    return four_sheet_groups, remaining_stage1, remaining_stage2


# STAGE 1: COMBINE REMAINING C=0 TWO-SHEET PAIRS WITH ONE UNMATCHED SHEET
# Allowed sequences: O-E-O, E-O-E, O-O-E, E-E-O.
# Stage 1 has no additional 25 mm intermediate allowance.
def combine_three_sheet_stage1_pairs(
    pair_table, unmatched_sheets, max_shear_length
):
    three_sheet_groups = []
    remaining_pairs = list(pair_table)
    remaining_sheets = sorted(unmatched_sheets, key=lambda item: item[0])

    if not remaining_sheets:
        return three_sheet_groups, remaining_pairs, remaining_sheets

    max_unmatched_length = max(sheet[2] for sheet in remaining_sheets)
    used_pair_indices = set()
    used_sheet_numbers = set()

    allowed_sequences = {
        ("O", "E", "O"),
        ("E", "O", "E"),
        ("O", "O", "E"),
        ("E", "E", "O"),
    }

    for pair_index, pair in enumerate(remaining_pairs):
        sh1_no = pair["sh1_no"]
        sh2_no = pair["sh2_no"]
        c_value = float(pair["c_value"])

        # Stage 1 three-sheet matching requires a distinct C=0 two-sheet pair.
        if sh1_no == sh2_no or abs(c_value) > 1e-9:
            continue

        # Preliminary eligibility: H_2S + L_max + A < HEAL limit.
        # A = 0 mm in Stage 1.
        pair_heal_length = float(pair["shear_length"])
        if pair_heal_length + max_unmatched_length >= max_shear_length:
            continue

        for sheet in remaining_sheets:
            sh3_no = sheet[0]
            sh3_length = sheet[2]

            if sh3_no in used_sheet_numbers:
                continue

            sequence = tuple(
                "O" if number % 2 else "E"
                for number in (sh1_no, sh2_no, sh3_no)
            )
            if sequence not in allowed_sequences:
                continue

            # Individual Stage 1 three-sheet HEAL length; no 25 mm allowance.
            heal_length = (
                pair["sh1_length"] + pair["sh2_length"]
                + sh3_length + 70 + c_value
            )
            if heal_length > max_shear_length:
                continue

            three_sheet_groups.append({
                "sh1_no": sh1_no,
                "sh1_length": pair["sh1_length"],
                "sh2_no": sh2_no,
                "sh2_length": pair["sh2_length"],
                "sh3_no": sh3_no,
                "sh3_length": sh3_length,
                "c_value": c_value,
                "g_value": 0,
                "intermediate_allowance": 0,
                "heal_length": heal_length,
            })
            used_pair_indices.add(pair_index)
            used_sheet_numbers.add(sh3_no)
            break

    remaining_pairs = [
        pair for index, pair in enumerate(remaining_pairs)
        if index not in used_pair_indices
    ]
    remaining_sheets = [
        sheet for sheet in remaining_sheets
        if sheet[0] not in used_sheet_numbers
    ]
    return three_sheet_groups, remaining_pairs, remaining_sheets


# ============================================================
# COMBINE 2-SHEET PAIRS WITH UNMATCHED SHEETS INTO 3-SHEET GROUPS
# ============================================================

def combine_three_sheet_pairs(pair_table, unmatched_sheets, max_shear_length):

    # --------------------------------------------------------
    # STEP 1: INITIAL SETUP
    # --------------------------------------------------------

    threshold = (max_shear_length - 95) / 1.5

    three_sheet_groups = []
    remaining_pairs = list(pair_table)

    remaining_sheets = sorted(
        unmatched_sheets,
        key=lambda x: x[0]
    )

    # Maximum length among the unmatched sheets
    if remaining_sheets:
        max_unmatched_length = max(
            sheet[2] for sheet in remaining_sheets
        )
    else:
        return three_sheet_groups, remaining_pairs, remaining_sheets

    used_pairs = set()
    used_sheets = set()

    # --------------------------------------------------------
    # STEP 2: CHECK EACH 2-SHEET PAIR
    # --------------------------------------------------------

    for pair_index, pair in enumerate(remaining_pairs):

        # Do not add a third sheet when this pair references the same sheet
        # number for SH1 and SH2.
        if pair["sh1_no"] == pair["sh2_no"]:
            continue

        # Existing three-sheet method accepts C=0 pairs only.
        if abs(float(pair["c_value"])) > 1e-9:
            continue

        # NEW RULE: 3-sheet matching is allowed only for same-group pairs:
        # Odd-Odd or Even-Even. Do not extend Odd-Even / Even-Odd pairs,
        # because the remaining unmatched sheets contain both parities and
        # extending an alternating pair can leave one group unusable later.
        if pair["sh1_no"] % 2 != pair["sh2_no"] % 2:
            continue

        pair_shear_length = pair["shear_length"]

        # Condition 1: 2-sheet HEAL length must be within the threshold.
        if pair_shear_length > threshold:
            continue

        # Condition 2: Pair plus the longest unmatched sheet must fit the machine.
        if pair_shear_length + max_unmatched_length > max_shear_length:
            continue

        sh2_no = pair["sh2_no"]

        # ----------------------------------------------------
        # STEP 3: FIND A COMPATIBLE THIRD SHEET
        # ----------------------------------------------------

        for sheet in remaining_sheets:

            sh3_no = sheet[0]
            sh3_length = sheet[2]

            if sh3_no in used_sheets:
                continue

            # SH3 must have opposite parity to SH2
            if sh2_no % 2 == sh3_no % 2:
                continue

            # ------------------------------------------------
            # STEP 4: CALCULATE 3-SHEET HEAL LENGTH
            # ------------------------------------------------

            heal_length = (
                pair["sh1_length"]
                + pair["sh2_length"]
                + sh3_length
                + 70
                + 25
                + pair["c_value"]
            )

            # Final machine-length validation
            if heal_length > max_shear_length:
                continue

            # ------------------------------------------------
            # STEP 5: STORE THE VALID 3-SHEET GROUP
            # ------------------------------------------------

            three_sheet_groups.append({
                "sh1_no": pair["sh1_no"],
                "sh1_length": pair["sh1_length"],

                "sh2_no": pair["sh2_no"],
                "sh2_length": pair["sh2_length"],

                "sh3_no": sh3_no,
                "sh3_length": sh3_length,

                "c_value": pair["c_value"],
                "heal_length": heal_length
            })

            used_pairs.add(pair_index)
            used_sheets.add(sh3_no)

            # One unmatched sheet is assigned to this pair
            break

    # --------------------------------------------------------
    # STEP 6: COLLECT REMAINING PAIRS AND SHEETS
    # --------------------------------------------------------

    remaining_pairs = [
        pair
        for index, pair in enumerate(remaining_pairs)
        if index not in used_pairs
    ]

    remaining_sheets = [
        sheet
        for sheet in remaining_sheets
        if sheet[0] not in used_sheets
    ]

    return three_sheet_groups, remaining_pairs, remaining_sheets

# NEW THREE-SHEET METHOD: ODD-EVEN-ODD / EVEN-ODD-EVEN
# Uses opposite-parity two-sheet pairs with C within the Stage 2 limit.
def combine_three_sheet_opposite_parity_pairs(
    pair_table, unmatched_sheets, max_shear_length, c_limit
):
    three_sheet_groups = []
    remaining_pairs = list(pair_table)
    remaining_sheets = sorted(unmatched_sheets, key=lambda item: item[0])

    if not remaining_sheets:
        return three_sheet_groups, remaining_pairs, remaining_sheets

    threshold = (max_shear_length - 95) / 1.5
    max_unmatched_length = max(sheet[2] for sheet in remaining_sheets)
    used_pairs = set()
    used_sheets = set()

    for pair_index, pair in enumerate(remaining_pairs):
        sh1_no = pair["sh1_no"]
        sh2_no = pair["sh2_no"]
        c_value = float(pair["c_value"])

        # Do not extend repeated-sheet pairs or same-parity pairs here.
        if sh1_no == sh2_no or sh1_no % 2 == sh2_no % 2:
            continue
        if c_value < 0 or c_value > c_limit:
            continue

        pair_shear_length = pair["shear_length"]
        if pair_shear_length > threshold:
            continue
        if pair_shear_length + max_unmatched_length > max_shear_length:
            continue

        for sheet in remaining_sheets:
            sh3_no = sheet[0]
            sh3_length = sheet[2]
            if sh3_no in used_sheets:
                continue

            # SH2 and SH3 must have opposite parity: O-E-O or E-O-E.
            if sh2_no % 2 == sh3_no % 2:
                continue

            heal_length = (
                pair["sh1_length"] + pair["sh2_length"] + sh3_length
                + 70 + 25 + c_value
            )
            if heal_length > max_shear_length:
                continue

            three_sheet_groups.append({
                "sh1_no": sh1_no,
                "sh1_length": pair["sh1_length"],
                "sh2_no": sh2_no,
                "sh2_length": pair["sh2_length"],
                "sh3_no": sh3_no,
                "sh3_length": sh3_length,
                "c_value": c_value,
                "heal_length": heal_length,
            })
            used_pairs.add(pair_index)
            used_sheets.add(sh3_no)
            break

    remaining_pairs = [
        pair for index, pair in enumerate(remaining_pairs)
        if index not in used_pairs
    ]
    remaining_sheets = [
        sheet for sheet in remaining_sheets if sheet[0] not in used_sheets
    ]
    return three_sheet_groups, remaining_pairs, remaining_sheets


def apply_three_sheet_heal_grouping(three_sheet_groups, group_size):
    """Set each batch of three-sheet groups to its maximum HEAL length."""
    if not three_sheet_groups:
        return three_sheet_groups
    if group_size <= 0:
        raise ValueError("Group size must be greater than zero.")

    groups = [
        three_sheet_groups[i:i + group_size]
        for i in range(0, len(three_sheet_groups), group_size)
    ]
    if len(groups) > 1 and len(groups[-1]) < 3:
        groups[-2].extend(groups.pop())

    for group_number, group in enumerate(groups, start=1):
        max_heal_length = max(item["heal_length"] for item in group)
        for item in group:
            item["heal_group"] = group_number
            item["heal_length"] = max_heal_length
    return three_sheet_groups


# TWO-SHEET LIMIT FALLBACK
def run_limit_fallback(all_sheets, params):

    all_sheets = sorted(all_sheets, key=lambda sheet: sheet[0])
    max_shear_length = params["max_shear_length"]
    wnc = params["wnc"]

    # STEP 1: FIND THE MINIMUM-LENGTH SHEET (SH1)
    sh1 = min(all_sheets, key=lambda sheet: sheet[2])
    sh1_length = sh1[2]

    # Maximum candidate length using the 70 mm allowance.
    max_candidate_length = max_shear_length - 70 - sh1_length

    print("\n" + "=" * 65)
    print("                         TWO-SHEET LIMIT FALLBACK")
    print("=" * 65)
    print(f"Minimum-length reference sheet : {sh1[0]}")
    print(f"Reference sheet length         : {sh1_length:.2f} mm")
    print(f"Maximum eligible sheet length  : {max_candidate_length:.2f} mm")

    # STEP 2: FIND ELIGIBLE SHEETS
    eligible_sheets = [sheet for sheet in all_sheets
        if sheet[2] <= max_candidate_length]

    if len(eligible_sheets) < 2:
        print("\nNo eligible two-sheet matching range found.")
        print("Switching the basket to the single-sheet plan.")

        odd_sheets = [s for s in all_sheets if s[0] % 2 != 0]
        even_sheets = [s for s in all_sheets if s[0] % 2 == 0]

        run_single_sheet_plan(odd_sheets, even_sheets, params)
        return []

    print("Eligible sheet numbers:", [sheet[0] for sheet in eligible_sheets])

    # Accepted pairs and their final HEAL results.
    accepted_rows = []
    accepted_sheet_numbers = set()

    # HELPER: EVALUATE A MATCHING METHOD
    def evaluate_method(method, result, remaining_sheets):

        if result["no_match"]:
            return None

        matched_pairs = create_matched_pairs(
            result["matched_sheets"], method
        )

        pair_table = create_matched_sheet_table(
            matched_pairs,
            method,
            params["p"],
            wnc,
            params["tol"]
        )

        # Only accept pairs within the actual machine limit.
        valid_rows = [
            row for row in pair_table
            if row["shear_length"] <= max_shear_length
        ]

        matched_numbers = set()

        for row in valid_rows:
            matched_numbers.add(row["sh1_no"])
            matched_numbers.add(row["sh2_no"])

        # Only count sheets that actually belong to this
        # remaining set.
        remaining_numbers = {sheet[0] for sheet in remaining_sheets}
        matched_numbers &= remaining_numbers

        unmatched_percentage = (
            (len(remaining_numbers) - len(matched_numbers))
            / len(remaining_numbers) * 100
            if remaining_numbers else 0
        )

        return {
            "method": method,
            "result": result,
            "rows": valid_rows,
            "matched_numbers": matched_numbers,
            "unmatched_percentage": unmatched_percentage
        }

    # HELPER: ACCEPT PAIRS WITHOUT REUSING SHEETS
    def accept_candidate(candidate):

        if candidate is None or not candidate["rows"]:
            return False

        new_rows = []

        for row in candidate["rows"]:

            sh1_no = row["sh1_no"]
            sh2_no = row["sh2_no"]

            # Never use an already-accepted sheet again.
            if sh1_no in accepted_sheet_numbers:
                continue

            if sh2_no in accepted_sheet_numbers:
                continue

            new_rows.append(row)

        if not new_rows:
            return False

        for row in new_rows:
            accepted_rows.append(row)
            accepted_sheet_numbers.add(row["sh1_no"])
            accepted_sheet_numbers.add(row["sh2_no"])

        return True

    # STEP 3: STAGE 1 - EVALUATE ALL EXISTING METHODS
    print("\nEvaluating Stage 1 matching methods...")

    stage1_results = build_normal_results(
        eligible_sheets, 1, wnc
    )

    stage1_candidates = []

    for method, result in stage1_results.items():

        candidate = evaluate_method(
            method, result, eligible_sheets
        )

        if candidate and candidate["rows"]:
            stage1_candidates.append(candidate)

    # Prefer the method that actually leaves the fewest
    # eligible sheets unmatched after the machine-limit check.
    stage1_candidates.sort(
        key=lambda candidate: (
            candidate["unmatched_percentage"],
            candidate["result"]["unmatched_percentage"]
        )
    )

    for candidate in stage1_candidates:

        if accept_candidate(candidate):
            print("\nAccepted Stage 1 method:", candidate["method"])
            print(
                "Unmatched percentage:",
                f"{candidate['unmatched_percentage']:.2f}%"
            )
            break

    # STEP 4: STAGE 2 - OPPOSITE-DIRECTION METHODS ONLY
    stage2_number = 2

    while True:

        accepted_current = set(accepted_sheet_numbers)

        remaining_eligible = [
            sheet for sheet in eligible_sheets
            if sheet[0] not in accepted_current
        ]

        if len(remaining_eligible) < 2:
            break

        print(f"\nEvaluating fallback Stage {stage2_number}...")

        stage2_results = build_normal_results(
            remaining_eligible,
            stage2_number,
            wnc
        )

        # Exclude all same-direction methods.
        opposite_results = {
            method: result
            for method, result in stage2_results.items()
            if "Same Direction" not in method
            and not result["no_match"]
        }

        if not opposite_results:
            print("No opposite-direction matching methods available.")
            break

        # Preserve the existing Stage 2 C-limit and method-selection
        # rules, while trying the next-ranked method if its actual
        # formed pairs do not satisfy the machine limit.
        opposite_c_limit = params["p"] * 0.35

        allowable_results = {
            method: result
            for method, result in opposite_results.items()
            if result["c"] is not None
            and result["c"] <= opposite_c_limit
        }

        ranked_results = sorted(
            allowable_results.items(),
            key=lambda item: (
                item[1]["unmatched_percentage"],
                item[1]["c"]
            )
        )

        accepted_this_stage = False

        for method, result in ranked_results:

            candidate = evaluate_method(
                method, result, remaining_eligible
            )

            if accept_candidate(candidate):
                print("Accepted method:", method)
                print(
                    "Unmatched percentage:",
                    f"{candidate['unmatched_percentage']:.2f}%"
                )
                accepted_this_stage = True
                break

        if not accepted_this_stage:
            print("No further valid opposite-direction matches found.")
            break

        stage2_number += 1

    # STEP 5: PREPARE FINAL TWO-SHEET RESULTS
    fallback_heal_results = collect_heal_results(
        [], accepted_rows, "Limit Fallback"
    )

    print("\nAccepted fallback two-sheet pairs:", len(accepted_rows))

    if fallback_heal_results:
        display_final_heal_table(fallback_heal_results)

    # STEP 6: SEND ONLY UNMATCHED SHEETS TO SINGLE-SHEET PLAN
    remaining_sheets = [
        sheet for sheet in all_sheets
        if sheet[0] not in accepted_sheet_numbers
    ]

    if remaining_sheets:

        print("\nRemaining unmatched sheet numbers:")
        print([sheet[0] for sheet in remaining_sheets])

        odd_remaining = [
            sheet for sheet in remaining_sheets
            if sheet[0] % 2 != 0
        ]

        even_remaining = [
            sheet for sheet in remaining_sheets
            if sheet[0] % 2 == 0
        ]

        run_single_sheet_plan(
            odd_remaining,
            even_remaining,
            params
        )

    return fallback_heal_results

# MAIN MATCHING PROCESS
def run_matching(odd_sheets, even_sheets, params):
    current_sheets = sorted(odd_sheets + even_sheets, key=lambda x: x[0])
    wnc = params["wnc"]
    stage = 1
    stage_tables = []
    all_heal_results = []
    stage1_pending_pairs = []
    stage1_pending_available = False

    while current_sheets:
        results = build_normal_results(current_sheets, stage, wnc)
        display_comparison(results, stage)
        selected = select_normal_method(results, stage)

        # NORMAL MATCHING FAILED: preserve held Stage 1 pairs before residual work.
        if selected is None:
            if stage1_pending_pairs:
                all_heal_results.extend(
                    collect_heal_results([], stage1_pending_pairs, 1)
                )
                stage1_pending_pairs = []
                stage1_pending_available = False

            print("\nNo allowable normal matching method found.")
            print("Entering Final Residual Matching")
            residual_solution = find_best_residual(current_sheets, wnc)

            if residual_solution is None:
                print("\nFinal Residual Matching failed.")
                print("Unable to match all remaining sheets.")
                break

            display_residual_result(residual_solution)
            residual_stage_results = residual_solution[3]

            for residual_index, residual_stage in enumerate(
                residual_stage_results, start=1
            ):
                residual_method = residual_stage["method"]
                residual_matched_sheets = residual_stage["matched_sheets"]
                residual_pairs = create_matched_pairs(
                    residual_matched_sheets, residual_method
                )
                residual_table = create_matched_sheet_table(
                    residual_pairs, residual_method,
                    params["p"], params["wnc"], params["tol"]
                )

                four_sheet_groups = []
                if "Same Direction" not in residual_method:
                    four_sheet_groups, residual_table = combine_four_sheet_pairs(
                        residual_table,
                        params["max_shear_length"],
                        params["qty"]
                    )

                residual_heal_results = collect_heal_results(
                    four_sheet_groups, residual_table,
                    f"Residual {residual_index}"
                )
                all_heal_results.extend(residual_heal_results)
                stage_tables.append(("Residual", residual_table))

            print("\n" + "=" * 60)
            print("       ALL RESIDUAL SHEETS SUCCESSFULLY MATCHED")
            print("=" * 60)
            break

        # NORMAL MATCHING SUCCESSFUL
        best_method, best_result = selected
        display_best_result(stage, best_result)

        matched_sheets = best_result["matched_sheets"]
        matched_pairs = create_matched_pairs(matched_sheets, best_method)
        matched_table = create_matched_sheet_table(
            matched_pairs, best_method,
            params["p"], params["wnc"], params["tol"]
        )

        four_sheet_groups = []
        if stage == 1 and "Same Direction" not in best_method:
            # Stage 1: combine two distinct Stage 1 two-sheet pairs.
            # Stage 1 four-sheet function is intentionally preserved.
            four_sheet_groups, matched_table = combine_four_sheet_pairs(
                matched_table,
                params["max_shear_length"],
                params["qty"]
            )

        # STAGE 1: after the existing Stage 1 four-sheet pass, attempt
        # C=0 three-sheet matching before carrying eligible pairs forward.
        if stage == 1:
            unmatched_sheets = get_unmatched_sheets(
                current_sheets, best_result["matched_sheets"]
            )

            print("\nAttempting Stage 1 C=0 three-sheet matching...")
            three_sheet_groups, matched_table, unmatched_sheets = (
                combine_three_sheet_stage1_pairs(
                    matched_table,
                    unmatched_sheets,
                    params["max_shear_length"]
                )
            )
            print("Stage 1 three-sheet groups formed:", len(three_sheet_groups))

            if three_sheet_groups:
                three_sheet_groups = apply_three_sheet_heal_grouping(
                    three_sheet_groups, params["group_size"]
                )
                print(
                    "Stage 1 SH3 sheet numbers assigned:",
                    [group["sh3_no"] for group in three_sheet_groups]
                )

            # Pairs not used for Stage 1 three-sheet matching remain eligible
            # for the cross-stage Stage 2 four-sheet check if they satisfy C=0.
            stage1_pending_pairs = []
            stage1_final_pairs = []
            can_defer = "Same Direction" not in best_method

            for pair in matched_table:
                pair = dict(pair)
                pair["_source_stage"] = 1
                if (
                    can_defer
                    and abs(float(pair["c_value"])) <= 1e-9
                    and pair["sh1_no"] != pair["sh2_no"]
                ):
                    stage1_pending_pairs.append(pair)
                else:
                    stage1_final_pairs.append(pair)

            matched_table = stage1_final_pairs
            stage1_pending_available = bool(stage1_pending_pairs)

        else:
            # Tag Stage 2 pairs so unmatched rows can be returned to their
            # originating stage after cross-stage and three-sheet matching.
            for pair in matched_table:
                pair["_source_stage"] = 2

            three_sheet_groups = []
            unmatched_sheets = get_unmatched_sheets(
                current_sheets, best_result["matched_sheets"]
            )

            # Stage 2 four-sheet pass: first use the current Stage 2 pairs
            # among themselves (the existing method), then combine remaining
            # Stage 1 C=0 pairs with Stage 2 candidate pairs.
            if stage == 2 and stage1_pending_pairs:
                if "Same Direction" not in best_method:
                    stage2_four_groups, remaining_stage1, remaining_stage2 = (
                        combine_stage2_four_sheet_pairs(
                            stage1_pending_pairs,
                            matched_table,
                            params["max_shear_length"],
                            params["qty"],
                            25.0
                        )
                    )
                    four_sheet_groups.extend(stage2_four_groups)
                    stage1_pending_pairs = remaining_stage1
                    matched_table = remaining_stage2
                    print(
                        "Additional Stage 2 four-sheet groups formed:",
                        len(stage2_four_groups)
                    )
                else:
                    # Same-direction Stage 2 pairs are not eligible for this
                    # opposite-direction cross-stage matching method.
                    matched_table = list(matched_table)

            # Combine all remaining pairs for the two ordered three-sheet passes.
            # Stage 1 pairs are tried too, because they are still available pairs.
            if stage == 2:
                if "Same Direction" not in best_method and matched_table or (
                    "Same Direction" not in best_method and stage1_pending_pairs
                ):
                    pairs_for_three = list(stage1_pending_pairs) + list(matched_table)

                    print("\nAttempting existing C=0 three-sheet matching...")
                    three_sheet_groups, pairs_for_three, unmatched_sheets = (
                        combine_three_sheet_pairs(
                            pairs_for_three,
                            unmatched_sheets,
                            params["max_shear_length"]
                        )
                    )
                    print("C=0 three-sheet groups formed:", len(three_sheet_groups))

                    # Then try opposite-parity pairs with allowable C.
                    if pairs_for_three and unmatched_sheets:
                        print("\nAttempting allowable-C alternating three-sheet matching...")
                        nonzero_c_groups, pairs_for_three, unmatched_sheets = (
                            combine_three_sheet_opposite_parity_pairs(
                                pairs_for_three,
                                unmatched_sheets,
                                params["max_shear_length"],
                                params["p"] * 0.35
                            )
                        )
                        three_sheet_groups.extend(nonzero_c_groups)
                        print(
                            "Allowable-C alternating three-sheet groups formed:",
                            len(nonzero_c_groups)
                        )

                    # Keep the leftover pairs separated by their original stage.
                    stage1_pending_pairs = [
                        pair for pair in pairs_for_three
                        if pair.get("_source_stage", 2) == 1
                    ]
                    matched_table = [
                        pair for pair in pairs_for_three
                        if pair.get("_source_stage", 2) != 1
                    ]
                    if three_sheet_groups:
                        three_sheet_groups = apply_three_sheet_heal_grouping(
                            three_sheet_groups, params["group_size"]
                        )
                        print(
                            "SH3 sheet numbers assigned:",
                            [group["sh3_no"] for group in three_sheet_groups]
                        )

        # Check the machine limit against every remaining pair, including
        # deferred Stage 1 pairs, so holding them cannot bypass this check.
        limit_check_table = list(matched_table)
        if stage == 1:
            limit_check_table.extend(stage1_pending_pairs)
        elif stage == 2:
            limit_check_table.extend(stage1_pending_pairs)

        limit_exceeded = check_two_sheet_shear_limit(
            limit_check_table, params["max_shear_length"]
        )

        if limit_exceeded:
            defer_fallback = (
                stage == 1 and bool(stage1_pending_pairs)
            )
        
            if defer_fallback:
                print(
                    "\nStage 1: deferring the limit fallback "
                    "until Stage 2 matching has been attempted."
                )
            else:
                print("\n" + "=" * 60)
                print("       2-SHEET HEAL LENGTH LIMIT EXCEEDED")
                print("=" * 60)
                print(
                    "Maximum Machine Shearing Length:",
                    params["max_shear_length"], "mm"
                )
                print("Checking whether valid two-sheet matches remain possible.")
        
                all_basket_sheets = sorted(
                    odd_sheets + even_sheets,
                    key=lambda sheet: sheet[0]
                )
                run_limit_fallback(all_basket_sheets, params)
                return None

        # Record finalized Stage 1 pairs. Deferred Stage 1 pairs are recorded
        # only after Stage 2 has had its opportunity to use them.
        if stage == 1:
            stage_heal_results = collect_heal_results(
                four_sheet_groups, matched_table, 1,
                three_sheet_groups=three_sheet_groups
            )
            all_heal_results.extend(stage_heal_results)
            stage_tables.append((1, matched_table))
        else:
            if stage1_pending_pairs:
                all_heal_results.extend(
                    collect_heal_results([], stage1_pending_pairs, 1)
                )
                stage1_pending_pairs = []
                stage1_pending_available = False

            stage_heal_results = collect_heal_results(
                four_sheet_groups, matched_table, stage,
                three_sheet_groups=three_sheet_groups
            )
            all_heal_results.extend(stage_heal_results)
            stage_tables.append((stage, matched_table))

        current_sheets = get_unmatched_sheets(
            current_sheets, best_result["matched_sheets"]
        )
        used_sh3_numbers = {group["sh3_no"] for group in three_sheet_groups}
        if used_sh3_numbers:
            current_sheets = [
                sheet for sheet in current_sheets
                if sheet[0] not in used_sh3_numbers
            ]

        print("\nRemaining Sheet Nos.:")
        print([sheet[0] for sheet in current_sheets])
        stage += 1

    # If Stage 2 was never reached, do not lose held Stage 1 pairs.
    if stage1_pending_pairs:
        all_heal_results.extend(
            collect_heal_results([], stage1_pending_pairs, 1)
        )

    display_final_heal_table(all_heal_results)
    return all_heal_results

# CALCULATE MATERIAL WASTAGE PERCENTAGE
# Wastage % = (Total HEAL Cutting Length - Total Generated Sheet Length)
#            / Total HEAL Cutting Length * 100
# This compares the material consumed by HEAL cutting with the useful
# generated sheet length, using the same per-basket basis.
def calculate_wastage_percentage(odd_sheets, even_sheets, all_heal_results):
    total_sheet_length = sum(sheet[2] for sheet in odd_sheets + even_sheets)

    # Apply special weighting only to the HEAL length used in this
    # wastage calculation. The displayed/final HEAL cutting lengths remain unchanged.
    total_heal_length = 0.0
    half_weight_rows = 0
    quarter_weight_rows = 0

    for row in all_heal_results:
        heal_length = row["heal_length"]
        scheme = row.get("scheme")

        if (
            scheme == 2
            and row.get("sh1_no") is not None
            and row.get("sh1_no") == row.get("sh2_no")
        ):
            # Repeated two-sheet pair: count 50% of its HEAL length.
            total_heal_length += heal_length * 0.50
            half_weight_rows += 1

        elif (
            scheme == 4
            and row.get("sh1_no") is not None
            and row.get("sh1_no") == row.get("sh2_no")
            == row.get("sh3_no") == row.get("sh4_no")
        ):
            # All four sheet references are identical: count 25% of its HEAL length.
            total_heal_length += heal_length * 0.25
            quarter_weight_rows += 1

        else:
            total_heal_length += heal_length

    wastage_length = total_heal_length - total_sheet_length

    if total_heal_length <= 0:
        wastage_percentage = 0.0
    else:
        wastage_percentage = (wastage_length / total_heal_length) * 100

    print("\n" + "=" * 60)
    print("                 MATERIAL WASTAGE SUMMARY")
    print("=" * 60)
    print(f"Total Generated Sheet Length : {total_sheet_length:.2f} mm")
    print(f"Adjusted HEAL Cutting Length : {total_heal_length:.2f} mm")
    if half_weight_rows:
        print(f"2-sheet pairs weighted at 50%: {half_weight_rows}")
    if quarter_weight_rows:
        print(f"4-sheet groups weighted at 25%: {quarter_weight_rows}")
    print(f"Total Wastage Length         : {wastage_length:.2f} mm")
    print(f"Wastage Percentage           : {wastage_percentage:.2f} %")

    return {
        "total_sheet_length": total_sheet_length,
        "total_heal_length": total_heal_length,
        "wastage_length": wastage_length,
        "wastage_percentage": wastage_percentage,
        "half_weight_rows": half_weight_rows,
        "quarter_weight_rows": quarter_weight_rows,
    }


# MAIN PROGRAM
def main():
    params = calculate_parameters()
    display_inputs(params)

    odd_sheets, even_sheets = generate_sheets(params)
    display_sheets(odd_sheets, even_sheets)

    all_heal_results = run_matching(odd_sheets, even_sheets, params)
    if all_heal_results is not None:
        calculate_wastage_percentage(odd_sheets, even_sheets, all_heal_results)

# PROGRAM START
if __name__ == "__main__":
    main()