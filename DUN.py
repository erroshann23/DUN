# ============================================================
# DUN CUTTING PLAN
# ============================================================
# INPUT DATA
# ============================================================
# PROJECT INFORMATION
# ============================================================
Name = "Darlipalli"              # Project / Customer name
SO = "SO12121232131"             # Sale Order number
BktType = "Type_B"               # Type of the Basket
DNo = "D-13-54-00542"            # Drawing Number
# -----------------------------
# Coil Details
# -----------------------------
cw = 407                         # Coil width (mm)
ct = 0.8                         # Coil thickness (mm)
# -----------------------------
# Profile Details
# -----------------------------
hu = 3.10                        # Undulation height (mm)
hn = 8.9                         # Notch height (mm)
p = 71.7                         # Notch pitch (mm)
wn = 18.0                        # Notch width (mm)
# -----------------------------
# Basket Dimensions
# -----------------------------
qty = 24                         # Basket quantity
lbo = 509                        # Bottom outer length (mm)
lto = 669                        # Top outer length (mm)
ho = 911                         # Outer height (mm)
tbf = 5                          # Basket frame thickness (mm)
tf = 6                           # Filling tolerance (mm)
web = 51.58                      # Empty Basket weight (kg)
wmin = 250.48                    # Engg Minimum Basket weight (kg)
wmax = 263.66                    # Engg Maximum Basket weight (kg)
# -----------------------------
# Sheet Matching Tolerance
# -----------------------------
tol = 2                          # Allowable SHM tolerance (mm)

# ============================================================
# CALCULATE PARAMETERS
# ============================================================
def calculate_parameters():
    hp = hu + hn                           # Pair height = Undulation height + Notch height
    lb = lbo - 2 * tbf - tf                # Bottom sheet filling length
    lt = lto - 2 * tbf - tf                # Top sheet filling length
    h = ho - 2 * tbf - 3                   # Sheet filling height
    incr = (lt - lb) / h                   # Increment used for calculating sheet length
    shq = round(h / hp * 2)                # Total number of sheets generated for one basket
    wnc = wn + 0.0092857 * cw + 0.7142857  # Corrected notch width used in SHM calculation
    return {
        "hp": hp,
        "lb": lb,
        "lt": lt,
        "h": h,
        "incr": incr,
        "shq": shq,
        "wnc": wnc,
        "p": p,
        "tol": tol}
    
# ============================================================
# DISPLAY INPUTS AND CALCULATED PARAMETERS
# ============================================================
def display_inputs(params):
    print("=" * 60)
    print("                 DUN CUTTING PLAN")
    print("=" * 60)
    print("\n---------------- PROJECT DATA ----------------")
    print("Project Name       :", Name)
    print("SO Number          :", SO)
    print("Basket Type        :", BktType)
    print("Drawing Number     :", DNo)
    print("\n---------------- COIL DETAILS ----------------")
    print("Coil Width         :", cw, "mm")
    print("Coil Thickness     :", ct, "mm")
    print("\n---------------- PROFILE DETAILS -------------")
    print("Undulation Height  :", hu, "mm")
    print("Notch Height       :", hn, "mm")
    print("Notch Pitch        :", p, "mm")
    print("Notch Width        :", wn, "mm")
    print("\n---------------- BASKET DETAILS --------------")
    print("Basket Quantity     :", qty)
    print("Bottom Outer Length :", lbo, "mm")
    print("Top Outer Length    :", lto, "mm")
    print("Outer Height        :", ho, "mm")
    print("Frame Thickness     :", tbf, "mm")
    print("Filling Tolerance   :", tf, "mm")
    print("\n---------------- CALCULATED PARAMETERS -------")
    print("Pair Height         :", round(params["hp"], 2), "mm")
    print("Bottom Length       :", round(params["lb"], 2), "mm")
    print("Top Length          :", round(params["lt"], 2), "mm")
    print("Height              :", round(params["h"], 2), "mm")
    print("Tanθ (Increment)    :", round(params["incr"], 2))
    print("Sheet Quantity      :", params["shq"], "Nos")
    print("Corrected Notch W.  :", round(params["wnc"], 1), "mm")
    print("Empty Basket Weight :", web, "kg")
    print("Minimum Basket Weight :", wmin, "kg")
    print("Maximum Basket Weight :", wmax, "kg")
    print("Matching Tolerance  :", tol, "mm")

# ============================================================
# GENERATE SHEETS
# ============================================================
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

# ============================================================
# DISPLAY GENERATED SHEETS
# ============================================================
def display_sheets(odd_sheets, even_sheets):
    print("\n"+ "-" * 25 + " ODD SHEETS " + "-" * 25 + "    " + "-" * 25 + " EVEN SHEETS " + "-" * 24)
    print(f"{'Sheet No.':>15} "f"{'Location (mm)':>21} "f"{'Length (mm)':>20} "f"    " f"{'Sheet No.':>15} "
        f"{'Location (mm)':>21} " f"{'Length (mm)':>20}")
    print("-" * 62 + "    " + "-" * 62)
    max_rows = max(
        len(odd_sheets),
        len(even_sheets))

    for i in range(max_rows):
        # Odd sheet
        if i < len(odd_sheets):
            no, loc, length = odd_sheets[i]
            odd_text = (f"{no:>10} " f"{loc:>21.2f} " f"{length:>20.0f}")
        else:
            odd_text = ( f"{'':>10} " f"{'':>21} " f"{'':>20}")
        # Even sheet
        if i < len(even_sheets):
            no, loc, length = even_sheets[i]
            even_text = ( f"{no:>15} " f"{loc:>21.2f} " f"{length:>20.0f}")
        else:
            even_text = ( f"{'':>15} " f"{'':>21} " f"{'':>20}")
            
        print(odd_text + "    " + even_text)

# ============================================================
# GET UNMATCHED SHEETS
# ============================================================
def get_unmatched_sheets(all_sheets, matched_sheets):
    matched_numbers = {sheet[0]
        for sheet in matched_sheets}
    return [sheet
        for sheet in all_sheets
        if sheet[0] not in matched_numbers]

# ============================================================
# GET MATCHED SHEETS
# ============================================================
def get_match_range(all_sheets, reference_no, match_no, reverse):
    if reverse:
        return [sheet
            for sheet in all_sheets
            if match_no <= sheet[0] <= reference_no]
    return [sheet
        for sheet in all_sheets
        if reference_no <= sheet[0] <= match_no]

# ============================================================
# CALCULATE SHM / C
# ============================================================
def calculate_match_value(reference_length, sheet_length, odd_even, same_direction, wnc):
    # --------------------------------------------------------
    # SAME DIRECTION
    # --------------------------------------------------------
    if same_direction:
        if odd_even:
            c = sheet_length % p # C Formula for Odd-Even / Even-Odd
        else:            
            c = p - (sheet_length % p) # C Formula for Odd-Odd / Even-Even
        return c 
    # --------------------------------------------------------
    # OPPOSITE DIRECTION
    # --------------------------------------------------------
    if odd_even: # Odd-Even / Even-Odd
        shm = p - ((reference_length + sheet_length - wnc - p / 2) % p)
    else: # Odd-Odd / Even-Even
        shm = p - ((reference_length + sheet_length - wnc) % p)
    return shm

def calculate_pair_c_value(sh1_length, sh2_length, odd_even, same_direction, p, wnc, tol):    
    # ========================================================
    # SAME DIRECTION
    # ========================================================
    if same_direction:
        if odd_even: # Odd-Even / Even-Odd
            shm = sh2_length % p
        else: # Odd-Odd / Even-Even
            shm = p - (sh2_length % p)
    # ========================================================
    # OPPOSITE DIRECTION
    # ========================================================
    else:
        if odd_even: # Odd-Even / Even-Odd
            shm = p - ((sh1_length + sh2_length - wnc - p / 2) % p)
        else: # Odd-Odd / Even-Even
            shm = p - ((sh1_length + sh2_length - wnc) % p)
    # ========================================================
    # FINAL C VALUE
    # ========================================================
    if shm <= tol or (p - shm) <= tol:
        c_value = 0
    else:
        c_value = round(shm, 0)
    return c_value

def calculate_shear_length(sh1_length, sh2_length, c_value):
    """Calculate HEAL shear length for one matched SH1-SH2 pair."""
    shear_length = sh1_length + sh2_length + 70 + c_value
    return shear_length

def create_matched_pairs(matched_sheets, method):

    if not matched_sheets:
        return []
    # ---------------------------------------------------------
    # Identify method type
    # ---------------------------------------------------------
    is_odd_even = ("Odd-Even" in method or "Even-Odd" in method)

    # ---------------------------------------------------------
    # ODD-EVEN / EVEN-ODD
    # ---------------------------------------------------------

    if is_odd_even:

        odd_sheets = [sheet for sheet in matched_sheets
            if sheet[0] % 2 != 0]

        even_sheets = [sheet for sheet in matched_sheets
            if sheet[0] % 2 == 0]

        # Nothing to pair
        if not odd_sheets or not even_sheets:
            return []

        # Sort groups
        odd_sheets.sort(key=lambda x: x[0])
        even_sheets.sort(key=lambda x: x[0])

        # Largest sheet determines SH1 group
        largest_sheet = max(matched_sheets, key=lambda x: x[0])

        if largest_sheet[0] % 2 != 0:
            sh1_group = odd_sheets
            sh2_group = even_sheets
        else:
            sh1_group = even_sheets
            sh2_group = odd_sheets

        # SH1 → descending
        sh1_group = list(reversed(sh1_group))
        # SH2 → ascending
        sh2_group = list(sh2_group)
        # Pair until one group is exhausted
        pair_count = min(len(sh1_group), len(sh2_group))
        matched_pairs = []

        for i in range(pair_count):
            sh1 = sh1_group[i]
            sh2 = sh2_group[i]
            matched_pairs.append((sh1, sh2))
        return matched_pairs

    # ---------------------------------------------------------
    # ODD-ODD / EVEN-EVEN
    # ---------------------------------------------------------
    matched_sheets = sorted(matched_sheets, key=lambda x: x[0])
    total = len(matched_sheets)

    # ---------------------------------------------------------
    # EVEN NUMBER OF SHEETS
    # ---------------------------------------------------------
    if total % 2 == 0:
        half = total // 2
        sh1_group = matched_sheets[:half]
        sh2_group = list(reversed(matched_sheets[half:]))
        matched_pairs = []

        for sh1, sh2 in zip(sh1_group, sh2_group):
            matched_pairs.append((sh1, sh2))
        return matched_pairs

    # ---------------------------------------------------------
    # ODD NUMBER OF SHEETS
    # ---------------------------------------------------------

    else:
        half = total // 2
        sh1_group = matched_sheets[:half]

        # Middle sheet
        middle_sheet = matched_sheets[half]
        # Sheets after middle
        sh2_group = list(reversed(matched_sheets[half + 1:]))
        matched_pairs = []

        # Normal pairs
        for sh1, sh2 in zip(sh1_group,sh2_group):
            matched_pairs.append((sh1, sh2))

        # Middle sheet pairs with itself
        matched_pairs.append((middle_sheet, middle_sheet))
        return matched_pairs

def display_matched_sheet_table(stage_tables):
    print("\n" + "=" * 100)
    print(" "*20 + "Sheet Match & HEAL Shear Length Calculation")
    print("=" * 100)
    # --------------------------------------------------------
    # Table Header
    # --------------------------------------------------------
    print(f"{'SH1 No.':>10}" f"{'SH1 Length':>10}" f"{'SH2 No.':>15}" f"{'SH2 Length':>10}"
           f"{'Shear Length':>18}" f"{'C Value':>10}")
    print("-" * 100)

    # --------------------------------------------------------
    # Print every stage
    # --------------------------------------------------------

    for stage_number, table in stage_tables:
        if not table:
            continue
        for row in table:
            print(f"{row['sh1_no']:>6}" f"{row['sh1_length']:>10.0f}" f"{row['sh2_no']:>15}"
                  f"{row['sh2_length']:>10.0f}" f"{row['shear_length']:>18.0f}" f"{row['c_value']:>10.0f}")
        # ----------------------------------------------------
        # Blank row between stages
        # ----------------------------------------------------
        print()
    print("=" * 100)
    
# ============================================================
# GET METHOD NAME
# ============================================================
def get_method_name(reference_group, candidate_group, reverse, same_direction):

    reference_parity = ("Odd"
        if reference_group[0][0] % 2 != 0
        else "Even")

    candidate_parity = ("Odd"
        if candidate_group[0][0] % 2 != 0
        else "Even")

    direction = ("Last → First"
        if reverse
        else "First → Last")

    if same_direction:
        return (f"Same Direction " f"{reference_parity}-{candidate_parity} " f"{direction}")
        
    return (f"{reference_parity}-{candidate_parity} " f"{direction}")

# ============================================================
# MATCH SHEETS
# ============================================================
def match_sheets(reference_group, candidate_group, current_sheets, reverse, odd_even, same_direction, stage, wnc, residual=False):

    if not reference_group or not candidate_group:
        return {"best_match": None,
            "shm": None,
            "c": None,
            "matched": 0,
            "unmatched": len(current_sheets),
            "unmatched_percentage": 100,
            "matched_sheets": [],
            "no_match": True}
    
    # --------------------------------------------------------
    # Select reference sheet
    # --------------------------------------------------------
    if reverse:
        reference_sheet = reference_group[-1]
    else:
        reference_sheet = reference_group[0]
    reference_no = reference_sheet[0]
    reference_length = reference_sheet[2]
    valid_matches = []

    # --------------------------------------------------------
    # Check every candidate
    # --------------------------------------------------------
    for sheet in candidate_group:
        sheet_no = sheet[0]
        sheet_length = sheet[2]
                
        if not reverse: # First → Last
            if sheet_no < reference_no:
                continue
        else: # Last → First
            if sheet_no > reference_no:
                continue

        # ----------------------------------------------------
        # Calculate SHM / C
        # ----------------------------------------------------
        value = calculate_match_value(reference_length, sheet_length, odd_even, same_direction, wnc)
        shm = value
        c = value
        
        # ----------------------------------------------------
        # Stage 1
        # ----------------------------------------------------
        if stage == 1 and not residual:
            if (shm <= tol or (p - shm) <= tol):
                valid_matches.append((sheet_no, shm, c))

        # ----------------------------------------------------
        # Stage 2+ / Final Residual
        # ----------------------------------------------------
        else:
            valid_matches.append((sheet_no, shm, c))

    # --------------------------------------------------------
    # No valid candidate
    # --------------------------------------------------------
    if not valid_matches:
        return {"method": get_method_name(reference_group, candidate_group, reverse, same_direction),
            "reference_no": reference_no,
            "best_match": None,
            "shm": None,
            "c": None,
            "matched": 0,
            "unmatched": len(current_sheets),
            "unmatched_percentage": 100,
            "matched_sheets": [],
            "no_match": True}

    # --------------------------------------------------------
    # Select best candidate for this method
    # --------------------------------------------------------
    if same_direction: # Same-direction, Minimum C:
        best = min(valid_matches, key=lambda x: x[2])
    elif reverse: # Last → First:
        best = min(valid_matches, key=lambda x: x[0])
    else: # First → Last:
        best = max(valid_matches, key=lambda x: x[0])
    match_no = best[0]
    match_shm = best[1]
    match_c = best[2]

    # --------------------------------------------------------
    # Get actual matched sheets
    # --------------------------------------------------------
    matched_sheets = get_match_range(current_sheets, reference_no, match_no, reverse)
    matched = len(matched_sheets)
    total = len(current_sheets)
    unmatched = total - matched
    if total > 0:
        unmatched_percentage = (unmatched / total) * 100
    else:
        unmatched_percentage = 0
        
    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------
    return {"method": get_method_name(reference_group, candidate_group, reverse, same_direction),
        "reference_no": reference_no,
        "best_match": match_no,
        "shm": match_shm,
        "c": match_c,
        "matched": matched,
        "unmatched": unmatched,
        "unmatched_percentage": unmatched_percentage,
        "matched_sheets": matched_sheets,
        "no_match": False}

# ============================================================
# BUILD NORMAL MATCHING RESULTS
# ============================================================
def build_normal_results(current_sheets, stage, wnc):
    odd_sheets = [sheet
        for sheet in current_sheets
        if sheet[0] % 2 != 0]
    even_sheets = [sheet
        for sheet in current_sheets
        if sheet[0] % 2 == 0]
    results = {}

    # ========================================================
    # OPPOSITE DIRECTION
    # ========================================================
    # --------------------------------------------------------
    # Odd-Odd
    # --------------------------------------------------------
    if odd_sheets:
        results["Odd-Odd First → Last"] = match_sheets(odd_sheets, odd_sheets, current_sheets, False, False, False, stage, wnc)

        results["Odd-Odd Last → First"] = match_sheets(odd_sheets, odd_sheets, current_sheets, True, False, False, stage, wnc)

    # --------------------------------------------------------
    # Odd-Even / Even-Odd
    # --------------------------------------------------------
    if odd_sheets and even_sheets:
        results["Odd-Even First → Last"] = match_sheets(odd_sheets, even_sheets, current_sheets, False, True, False, stage, wnc)

        results["Odd-Even Last → First"] = match_sheets(odd_sheets, even_sheets, current_sheets, True, True, False, stage, wnc)

        results["Even-Odd First → Last"] = match_sheets(even_sheets, odd_sheets, current_sheets, False, True, False, stage, wnc)

        results["Even-Odd Last → First"] = match_sheets( even_sheets, odd_sheets, current_sheets, True, True, False, stage, wnc)

    # --------------------------------------------------------
    # Even-Even
    # --------------------------------------------------------
    if even_sheets:
        results["Even-Even First → Last"] = match_sheets(even_sheets, even_sheets, current_sheets, False, False, False, stage, wnc)

        results["Even-Even Last → First"] = match_sheets(even_sheets, even_sheets, current_sheets, True, False, False, stage, wnc)

    # ========================================================
    # SAME DIRECTION: starts from Stage 2.
    # ========================================================
    if stage >= 2:
        # ----------------------------------------------------
        # Odd-Odd
        # ----------------------------------------------------
        if odd_sheets:
            results["Same Direction Odd-Odd First → Last"
                ] = match_sheets( odd_sheets, odd_sheets, current_sheets, False, False, True, stage, wnc)

            results["Same Direction Odd-Odd Last → First"
                ] = match_sheets(odd_sheets, odd_sheets, current_sheets, True, False, True, stage, wnc)

        # ----------------------------------------------------
        # Odd-Even / Even-Odd
        # ----------------------------------------------------
        if odd_sheets and even_sheets:
            results["Same Direction Odd-Even First → Last"
                ] = match_sheets( odd_sheets, even_sheets, current_sheets, False, True, True, stage, wnc)
            results["Same Direction Odd-Even Last → First"
                ] = match_sheets( odd_sheets, even_sheets, current_sheets, True, True, True, stage, wnc)
            results["Same Direction Even-Odd First → Last"
                ] = match_sheets( even_sheets, odd_sheets, current_sheets, False, True, True, stage, wnc)
            results["Same Direction Even-Odd Last → First"
                ] = match_sheets(even_sheets, odd_sheets, current_sheets, True, True, True, stage, wnc)

        # ----------------------------------------------------
        # Even-Even
        # ----------------------------------------------------
        if even_sheets:
            results["Same Direction Even-Even First → Last"
                ] = match_sheets( even_sheets, even_sheets, current_sheets, False, False, True, stage, wnc)
            results[
                "Same Direction Even-Even Last → First"
                ] = match_sheets( even_sheets, even_sheets, current_sheets, True, False, True, stage, wnc)
    return results

# ============================================================
# SELECT NORMAL MATCHING METHOD
# ============================================================

def select_normal_method(results, stage):

    valid_results = {method: result
        for method, result in results.items()
        if not result["no_match"]}

    if not valid_results:
        return None

    # ========================================================
    # STAGE 1
    # ========================================================
    if stage == 1:
        return min(valid_results.items(), key=lambda x: x[1]["unmatched_percentage"])

    # ========================================================
    # STAGE 2+
    # ========================================================
    opposite_c_limit = p * 0.35
    same_c_limit = 20
    allowable_methods = {}
    for method, result in valid_results.items():
        c = result["c"]

        # ----------------------------------------------------
        # Same Direction C limit
        # ----------------------------------------------------
        if "Same Direction" in method:
            if c < same_c_limit:
                allowable_methods[method] = result

        # ----------------------------------------------------
        # Opposite Direction C limit
        # ----------------------------------------------------
        else:
            if c <= opposite_c_limit:
                allowable_methods[method] = result
    # No allowable method
    if not allowable_methods:
        return None

    # --------------------------------------------------------
    # Select: 1. Minimum unmatched %, 2. Minimum C
    # --------------------------------------------------------
    return min(allowable_methods.items(), key=lambda x: (x[1]["unmatched_percentage"], x[1]["c"]))

# ============================================================
# FINAL RESIDUAL - GENERATE ALL POSSIBLE OPTIONS
# ============================================================
def get_residual_options(current_sheets, wnc):
    current_sheets = sorted(current_sheets, key=lambda x: x[0])

    odd_sheets = [sheet
        for sheet in current_sheets
        if sheet[0] % 2 != 0]

    even_sheets = [sheet
        for sheet in current_sheets
        if sheet[0] % 2 == 0]

    # --------------------------------------------------------
    # Four parity combinations
    # --------------------------------------------------------
    groups = [("Odd-Odd", odd_sheets, odd_sheets, False),
              ("Odd-Even", odd_sheets, even_sheets, True),
              ("Even-Odd", even_sheets, odd_sheets, True),
              ("Even-Even", even_sheets, even_sheets, False)]
    options = []

    # ========================================================
    # Check all combinations
    # ========================================================
    for (pair_name, reference_group, candidate_group, odd_even) in groups:
        if not reference_group:
            continue
        if not candidate_group:
            continue

        # ----------------------------------------------------
        # First → Last AND Last → First
        # ----------------------------------------------------
        for reverse in (False, True):
            if reverse:
                reference_sheet = (reference_group[-1])
            else:
                reference_sheet = (reference_group[0])
            reference_no = reference_sheet[0]
            reference_length = reference_sheet[2]

            # ------------------------------------------------
            # Check every candidate
            # ------------------------------------------------
            for candidate in candidate_group:
                candidate_no = candidate[0]
                candidate_length = candidate[2]
                # First → Last
                if not reverse:
                    if candidate_no < reference_no:
                        continue
                # Last → First
                else:
                    if candidate_no > reference_no:
                        continue

                # --------------------------------------------
                # Opposite direction
                # --------------------------------------------
                c = calculate_match_value(reference_length, candidate_length, odd_even, False, wnc)

                matched_sheets = get_match_range(current_sheets, reference_no, candidate_no, reverse)

                if matched_sheets:
                    remaining_sheets = (get_unmatched_sheets(current_sheets, matched_sheets))

                    direction = ("Last → First"
                        if reverse
                        else "First → Last")

                    options.append({"method": f"{pair_name} {direction}",
                        "reference_no": reference_no,
                        "best_match": candidate_no,
                        "shm": c,
                        "c": c,
                        "matched": len(matched_sheets),
                        "unmatched": len(remaining_sheets),
                        "matched_sheets": matched_sheets,
                        "remaining_sheets": remaining_sheets})

                # --------------------------------------------
                # Same direction
                # --------------------------------------------
                c = calculate_match_value( reference_length, candidate_length, odd_even, True, wnc)
                if matched_sheets:
                    remaining_sheets = (get_unmatched_sheets( current_sheets, matched_sheets))

                    options.append({
                        "method": f"Same Direction " f"{pair_name} " f"{direction}",
                        "reference_no":reference_no,
                        "best_match": candidate_no,
                        "shm": c,
                        "c": c,
                        "matched": len(matched_sheets),
                        "unmatched": len(remaining_sheets),
                        "matched_sheets": matched_sheets,
                        "remaining_sheets": remaining_sheets })
    return options

# ============================================================
# FINAL RESIDUAL - FIND COMPLETE SOLUTION
# ============================================================
def find_best_residual(current_sheets, wnc):
    # --------------------------------------------------------
    # No sheets remaining
    # --------------------------------------------------------
    if not current_sheets:
        return (0, 0, 0,[])
    best_solution = None

    # --------------------------------------------------------
    # Generate every possible residual option
    # --------------------------------------------------------
    options = get_residual_options(current_sheets, wnc)

    # ========================================================
    # Try every option
    # ========================================================
    for option in options:
        remaining = (option["remaining_sheets"])

        # ----------------------------------------------------
        # Must actually remove sheets
        # ----------------------------------------------------
        if len(remaining) >= len(current_sheets):
            continue

        # ----------------------------------------------------
        # Solve remaining sheets
        # ----------------------------------------------------
        next_solution = find_best_residual(remaining, wnc)

        if next_solution is None:
            continue
            
        # ----------------------------------------------------
        # Calculate solution score
        # ----------------------------------------------------
        total_c = (option["c"] + next_solution[0])
        maximum_c = max(option["c"], next_solution[1])
        stages = (1 + next_solution[2])
        path = ([option] + next_solution[3])
        solution = (total_c, maximum_c, stages, path)

        # ----------------------------------------------------
        # Keep best complete solution
        # ----------------------------------------------------
        if best_solution is None:
            best_solution = solution
        else:
            current_score = (solution[0], solution[1], solution[2])
            best_score = (best_solution[0], best_solution[1], best_solution[2])
            
            if current_score < best_score:
                best_solution = solution
    return best_solution

# ============================================================
# DISPLAY NORMAL COMPARISON
# ============================================================
def display_comparison(results, stage):
    print("\n" + "=" * 60)
    print("             UNMATCHED SHEETS COMPARISON")
    print("=" * 60)

    for method, result in results.items():
        if stage == 1:
            print(f"{method:<45} : " f"{result['unmatched_percentage']:.2f} " f"% unmatched")
        else:
            if result["c"] is None:
                c_text = "No Match"
            else:
                c_text = (f"{result['c']:.2f} mm")
                
            print(f"{method:<50} : " f"{result['unmatched_percentage']:.2f} " f"% unmatched" f" | C = {c_text}")

# ============================================================
# DISPLAY BEST NORMAL RESULT
# ============================================================
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
    print("Matched Sheet Nos.  :", [sheet[0] for sheet in result["matched_sheets"]])

# ============================================================
# DISPLAY FINAL RESIDUAL RESULT
# ============================================================
def display_residual_result(solution):
    total_c = solution[0]
    maximum_c = solution[1]
    stages = solution[2]
    path = solution[3]

    # ========================================================
    # FINAL RESIDUAL HEAL TABULATION
    # ========================================================
    print("\n" + "=" * 60)
    print("             FINAL RESIDUAL MATCHING")
    print("=" * 60)
    print("Residual Stages     :", stages)
    print("Total C             :", f"{total_c:.2f} mm")
    print("Maximum C           :", f"{maximum_c:.2f} mm")

    # --------------------------------------------------------
    # Display each residual stage
    # --------------------------------------------------------
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
        print("Matched Sheet Nos.  :", [sheet[0] for sheet in result["matched_sheets"]])
        print("Remaining Sheet Nos.:", [sheet[0] for sheet in result["remaining_sheets"]])
def create_matched_sheet_table(matched_pairs, method, p, wnc, tol):
    same_direction = "Same Direction" in method
    if "Odd-Even" in method or "Even-Odd" in method:
        odd_even = True
    else:
        odd_even = False

    table = []

    for sh1, sh2 in matched_pairs:
        sh1_no = sh1[0]
        sh1_length = sh1[2]

        sh2_no = sh2[0]
        sh2_length = sh2[2]
        c_value = calculate_pair_c_value(sh1_length, sh2_length, odd_even, same_direction, p, wnc, tol)
        shear_length = calculate_shear_length(sh1_length, sh2_length, c_value)

        table.append({
            "sh1_no": sh1_no,
            "sh1_length": sh1_length,
            "sh2_no": sh2_no,
            "sh2_length": sh2_length,
            "shear_length": shear_length,
            "c_value": c_value})
    return table

# ============================================================
# MAIN MATCHING PROCESS
# ============================================================
def run_matching(odd_sheets, even_sheets, params):
    # ========================================================
    # INITIAL SETUP
    # ========================================================
    current_sheets = odd_sheets + even_sheets
    current_sheets.sort(key=lambda x: x[0])
    wnc = params["wnc"]
    stage = 1
    # Store HEAL tables from every stage
    stage_tables = []

    # ========================================================
    # MATCHING LOOP
    # ========================================================
    while current_sheets:
        # ----------------------------------------------------
        # Build normal matching results for current stage
        # ----------------------------------------------------
        results = build_normal_results(current_sheets, stage, wnc)
        display_comparison(results, stage)

        # ----------------------------------------------------
        # Select allowable normal matching method
        # ----------------------------------------------------
        selected = select_normal_method(results, stage)

        # ====================================================
        # NORMAL MATCHING FAILED
        # ====================================================
        if selected is None:

            print("\nNo allowable normal matching method found.")
            print("Entering Final Residual Matching")

            residual_solution = find_best_residual(current_sheets, wnc)

            if residual_solution is None:
                print("\nFinal Residual Matching failed.")
                print("Unable to match all remaining sheets.")
                break

            display_residual_result(residual_solution)

            residual_stage_results = residual_solution[3]

            for residual_stage in residual_stage_results:
                residual_method = residual_stage["method"]
                residual_matched_sheets = (residual_stage["matched_sheets"])
                residual_pairs = create_matched_pairs(residual_matched_sheets, residual_method)
                residual_table = create_matched_sheet_table(residual_pairs, residual_method, params["p"], params["wnc"], params["tol"])
                stage_tables.append(("Residual", residual_table))
                
            print("\n" + "=" * 60)
            print("       ALL RESIDUAL SHEETS SUCCESSFULLY MATCHED")
            print("=" * 60)
            break
            
        # ====================================================
        # NORMAL MATCHING SUCCESSFUL
        # ====================================================
        best_method, best_result = selected
        display_best_result(stage, best_result)

        # ----------------------------------------------------
        # Get sheets matched in this stage
        # ----------------------------------------------------
        matched_sheets = best_result["matched_sheets"]

        # ----------------------------------------------------
        # Create SH1-SH2 pairs
        # ----------------------------------------------------
        matched_pairs = create_matched_pairs(matched_sheets, best_method)

        # ----------------------------------------------------
        # Create HEAL table for this stage
        # ----------------------------------------------------
        matched_table = create_matched_sheet_table(matched_pairs, best_method, params["p"], params["wnc"], params["tol"])

        # ----------------------------------------------------
        # Store stage table
        # ----------------------------------------------------
        stage_tables.append((stage, matched_table))

        # ----------------------------------------------------
        # Remove matched sheets
        # ----------------------------------------------------
        current_sheets = get_unmatched_sheets(current_sheets, best_result["matched_sheets"])
        print("\nRemaining Sheet Nos.:")
        print([sheet[0] for sheet in current_sheets])
        
        # ----------------------------------------------------
        # Move to next stage
        # ----------------------------------------------------
        stage += 1
    # ========================================================
    # DISPLAY COMPLETE HEAL MATCHED SHEET TABLE
    # ========================================================
    display_matched_sheet_table(stage_tables)

# ============================================================
# MAIN PROGRAM
# ============================================================
def main():
    # --------------------------------------------------------
    # Calculate parameters
    # --------------------------------------------------------
    params = calculate_parameters()
    # --------------------------------------------------------
    # Display inputs
    # --------------------------------------------------------
    display_inputs(params)
    # --------------------------------------------------------
    # Generate sheets
    # --------------------------------------------------------
    odd_sheets, even_sheets = generate_sheets(params)
    # --------------------------------------------------------
    # Display sheets
    # --------------------------------------------------------
    display_sheets(odd_sheets, even_sheets)
    # --------------------------------------------------------
    # Run matching
    # --------------------------------------------------------
    run_matching(odd_sheets, even_sheets, params)

# ============================================================
# PROGRAM START
# ============================================================
if __name__ == "__main__":
    main()