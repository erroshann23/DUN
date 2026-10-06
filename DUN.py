# ============================================================
# DUN CUTTING PLAN
# ============================================================
# INPUT DATA
# ============================================================
# -----------------------------
# Project Information
# -----------------------------
Name = "Darlipalli"              # Project / Customer name
SO = "SO12121232131"             # Sale Order number
BktType = "Type_B"               # Type of the Basket
DNo = "D-13-54-00542"            # Drawing Number

# -----------------------------
# Coil Details
# -----------------------------
cw = 406                         # Coil width (mm)
ct = 0.8                         # Coil thickness (mm)

# -----------------------------
# Profile Details
# -----------------------------
hu = 3.45                        # Undulation height (mm)
hn = 9.3                         # Notch height (mm)
p = 71.7                         # Notch pitch (mm)
wn = 18.0                        # Notch width (mm)

# -----------------------------
# Basket Dimensions
# -----------------------------
qty = 2                          # Basket quantity
lbo = 746                        # Bottom outer length (mm)
lto = 905                        # Top outer length (mm)
ho = 910                         # Outer height (mm)
tbf = 4                          # Basket frame thickness (mm)
tf = 3                           # Filling tolerance (mm)
web = 51.58                      # Empty Basket weight (kg)
wmin = 250.48                    # Engg Minimum Basket weight (kg)
wmax = 263.66                    # Engg Maximum Basket weight (kg)

# -----------------------------
# Sheet Matching Tolerance
# -----------------------------
tol = 2                          # Allowable SHM tolerance (mm)

# ============================================================
# CALCULATED PARAMETERS
# ============================================================
hp = hu + hn                           # Pair height = Undulation height + Notch height
lb = lbo - 2 * tbf - tf                # Bottom sheet filling length
lt = lto - 2 * tbf - tf                # Top sheet filling length
h = ho - 2 * tbf - 3                   # Sheet filling height
incr = (lt - lb) / h                   # Increment used for calculating sheet length
shq = round(h / hp * 2)                # Total number of sheets generated for one basket
wnc = wn + 0.0092857 * cw + 0.7142857  # Corrected notch width used in SHM calculation

# ============================================================
# DISPLAY INPUTS AND CALCULATED PARAMETERS
# ============================================================
print("============================================================")
print("                 DUN CUTTING PLAN")
print("============================================================")
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
print("Pair Height         :", round(hp, 2), "mm")
print("Bottom Length       :", round(lb, 2), "mm")
print("Top Length          :", round(lt, 2), "mm")
print("Height              :", round(h, 2), "mm")
print("Tanθ (Increment)    :", round(incr, 2))
print("Sheet Quantity      :", shq, "Nos")
print("Corrected Notch W.  :", round(wnc, 1), "mm")
print("Empty Basket Weight :",web, "kg")
print("Minimum Basket Weight :",wmin, "kg")
print("Maximum Basket Weight :",wmax, "kg")
print("Matching Tolerance  :", tol, "mm")

# ============================================================
# SHEET GENERATION
# ============================================================
# Lists used to store generated sheets
# Each sheet is stored as: (Sheet Number, Sheet Location, Sheet Length)
odd_sheets = []
even_sheets = []
# Generate every sheet from 1 to total sheet quantity
for i in range(1, shq + 1):   
    shloc = hn / 2 + (i - 1) * hp / 2 # Sheet location measured from the bottom of the basket
    shl = lb + shloc * incr # Sheet length calculated from bottom length and slope
    # Separate sheets into Odd and Even groups
    if i % 2 == 0:
        even_sheets.append((i, shloc, shl)) # Even-numbered sheet
    else: 
        odd_sheets.append((i, shloc, shl)) # Odd-numbered sheet        

# ============================================================
# DISPLAY ODD AND EVEN SHEETS
# ============================================================
print("\n" + "-" * 25 + " ODD SHEETS " + "-" * 25 + "    " + "-" * 25 + " EVEN SHEETS " + "-" * 24)
print(f"{'Sheet No.':>15} {'Location (mm)':>21} {'Length (mm)':>20}" f"    "
    f"{'Sheet No.':>15} {'Location (mm)':>21} {'Length (mm)':>20}")
print("-" * 62+"    "+"-"* 62)
# max() allows the code to work even when the number of odd and even sheets are not exactly the same.
max_rows = max(len(odd_sheets), len(even_sheets))
for i in range(max_rows):
    # Odd-sheet data
    if i < len(odd_sheets):
        odd_no = odd_sheets[i][0]
        odd_loc = odd_sheets[i][1]
        odd_len = odd_sheets[i][2]
        odd_text = (
            f"{odd_no:>10} "
            f"{odd_loc:>21.2f} "
            f"{odd_len:>20.0f}")
    else:
        odd_text = f"{'':>10} {'':>21} {'':>20}"
    # Even-sheet data
    if i < len(even_sheets):
        even_no = even_sheets[i][0]
        even_loc = even_sheets[i][1]
        even_len = even_sheets[i][2]
        even_text = (
            f"{even_no:>15} "
            f"{even_loc:>21.2f} "
            f"{even_len:>20.0f}")
    else:
        even_text = f"{'':>15} {'':>21} {'':>20}"        
    print(odd_text + "    " + even_text)

# ============================================================
# SHEET MATCHING FUNCTION
# ============================================================
def match_sheets(reference_group, candidate_group,
                 all_current_sheets,
                 reverse=False,
                 odd_even=False,
                 same_direction=False,
                 stage=1,
                 final_residual=False):
   
    # --------------------------------------------------------
    # Select reference sheet
    # --------------------------------------------------------
    if reverse:
        reference_sheet = reference_group[-1]
        direction = "Last → First"
    else:
        reference_sheet = reference_group[0]
        direction = "First → Last"

    reference_no = reference_sheet[0]
    reference_length = reference_sheet[2]
    
    # --------------------------------------------------------
    # Set candidate direction
    # --------------------------------------------------------
    if reverse:
        candidates = reversed(candidate_group)
    else:
        candidates = candidate_group

    valid_matches = []
    # --------------------------------------------------------
    # Check every candidate
    # --------------------------------------------------------
    for sheet in candidates:
        sheet_no = sheet[0]
        sheet_length = sheet[2]
        
        # ====================================================
        # OPPOSITE DIRECTION MATCHING
        # ====================================================
        if not same_direction:
            if odd_even:
                # Odd-Even / Even-Odd
                shm = p - ((reference_length + sheet_length - wnc - p / 2) % p)
            else:
                # Odd-Odd / Even-Even
                shm = p - ((reference_length + sheet_length - wnc) % p)
            c = shm

            if final_residual:
                valid_matches.append((sheet_no, shm, c))            
            # ------------------------------------------------
            # Stage 1
            # ------------------------------------------------
            elif stage == 1:
                if final_residual or shm <= tol or (p - shm) <= tol:
                    valid_matches.append((sheet_no, shm, c))
            
            # ------------------------------------------------
            # Stage 2 onwards Existing opposite-direction logic
            # ------------------------------------------------
            else:
                c_limit = p * 0.35
                # Normal Stage 2+ matching
                if c < c_limit:
                    valid_matches.append((sheet_no, shm, c))
                # Self-match is allowed from Stage 2 onwards
                elif sheet_no == reference_no:
                    valid_matches.append((sheet_no, shm, c))
        
        # ====================================================
        # SAME DIRECTION MATCHING
        # ====================================================
        else:
            if odd_even:
                # Odd-Even / Even-Odd
                c = sheet_length % p
            else:
                # Odd-Odd / Even-Even
                c = p - (sheet_length % p)
            # For same-direction matching,
            # C itself is the matching condition.
            shm = c
            # Same-direction approval condition
            if final_residual or c < 20:
                valid_matches.append((sheet_no, shm, c))
    
    # --------------------------------------------------------
    # Find best candidate
    # --------------------------------------------------------
    if valid_matches:
        if not same_direction:
            # Existing opposite-direction selection
            if reverse:
                best_match = min(valid_matches,key=lambda x: x[0])
            else:
                best_match = max(valid_matches,key=lambda x: x[0])
        else:
            # Same-direction:
            # select minimum C
            best_match = min(valid_matches,key=lambda x: x[2])
        match_no = best_match[0]
        match_shm = best_match[1]
        match_c = best_match[2]
    else:
        match_no = None
        match_shm = None
        match_c = None
   
    # --------------------------------------------------------
    # Determine actual matched sheets from CURRENT sheet list
    # --------------------------------------------------------
    if match_no is not None:
        if reverse:
            matched_sheets = [sheet
                for sheet in all_current_sheets
                if match_no <= sheet[0] <= reference_no]
        else:
            matched_sheets = [sheet
                for sheet in all_current_sheets
                if reference_no <= sheet[0] <= match_no]
    else:
        matched_sheets = []
    
    # --------------------------------------------------------
    # Calculate counts
    # --------------------------------------------------------
    matched = len(matched_sheets)
    total_sheets = len(all_current_sheets)
    unmatched = total_sheets - matched
    if unmatched < 0:
        unmatched = 0

    # --------------------------------------------------------
    # Calculate unmatched percentage
    # --------------------------------------------------------
    if total_sheets > 0:
        unmatched_percentage = (unmatched / total_sheets) * 100
    else:
        unmatched_percentage = 0

    # --------------------------------------------------------
    # Match type
    # --------------------------------------------------------
    if odd_even:
        match_type = "Odd → Even"
    else:
        match_type = "Odd → Odd"

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------
    return {
        "type": match_type,
        "direction": direction,
        "reference_no": reference_no,
        "reference_length": reference_length,
        "best_match": match_no,
        "shm": match_shm,
        "c": match_c,
        "matched": matched,
        "unmatched": unmatched,
        "unmatched_percentage": unmatched_percentage,
        "matched_sheets": matched_sheets,
        "no_match": match_no is None
    }

def get_unmatched_sheets(all_sheets, matched_sheets):
    matched_numbers = {
        sheet[0] for sheet in matched_sheets}
    unmatched_sheets = [
        sheet for sheet in all_sheets
        if sheet[0] not in matched_numbers]
    return unmatched_sheets

# ============================================================
# REPEATED SHEET MATCHING
# ============================================================
# Start with all generated sheets
current_sheets = (odd_sheets + even_sheets)
# Sort by sheet number
current_sheets.sort(key=lambda x: x[0])
stage = 1
final_residual = False
while len(current_sheets) > 0:
    print("\n============================================================")
    print(f"                    MATCHING STAGE {stage}")
    print("============================================================")

    current_odd_sheets = [
        sheet for sheet in current_sheets # Separated Odd sheets
        if sheet[0] % 2 != 0]
    current_even_sheets = [
        sheet for sheet in current_sheets # Separated Even sheets
        if sheet[0] % 2 == 0]
    matching_results = {} # Store all possible matching results 
    
    # ========================================================
    # STAGE:1 OPPOSITE DIRECTION MATCHING
    # ========================================================
    
    # ========================================================
    # ODD → ODD
    # ========================================================
    
    if len(current_odd_sheets) > 0:
    
        matching_results["Odd-Odd First → Last"] = match_sheets(
            current_odd_sheets,
            current_odd_sheets,
            current_sheets,
            reverse=False,
            odd_even=False,
            same_direction=False,
            stage=stage
        )
    
        matching_results["Odd-Odd Last → First"] = match_sheets(
            current_odd_sheets,
            current_odd_sheets,
            current_sheets,
            reverse=True,
            odd_even=False,
            same_direction=False,
            stage=stage
        )
    
    
    # ========================================================
    # ODD → EVEN
    # ========================================================
    
    if (
        len(current_odd_sheets) > 0
        and len(current_even_sheets) > 0
    ):
    
        matching_results["Odd-Even First → Last"] = match_sheets(
            current_odd_sheets,
            current_even_sheets,
            current_sheets,
            reverse=False,
            odd_even=True,
            same_direction=False,
            stage=stage
        )
    
        matching_results["Odd-Even Last → First"] = match_sheets(
            current_odd_sheets,
            current_even_sheets,
            current_sheets,
            reverse=True,
            odd_even=True,
            same_direction=False,
            stage=stage
        )
    
    
    # ========================================================
    # EVEN → ODD
    # ========================================================
    
    if (
        len(current_even_sheets) > 0
        and len(current_odd_sheets) > 0
    ):
    
        matching_results["Even-Odd First → Last"] = match_sheets(
            current_even_sheets,
            current_odd_sheets,
            current_sheets,
            reverse=False,
            odd_even=True,
            same_direction=False,
            stage=stage
        )
    
        matching_results["Even-Odd Last → First"] = match_sheets(
            current_even_sheets,
            current_odd_sheets,
            current_sheets,
            reverse=True,
            odd_even=True,
            same_direction=False,
            stage=stage
        )
    
    
    # ========================================================
    # EVEN → EVEN
    # ========================================================
    
    if len(current_even_sheets) > 0:
    
        matching_results["Even-Even First → Last"] = match_sheets(
            current_even_sheets,
            current_even_sheets,
            current_sheets,
            reverse=False,
            odd_even=False,
            same_direction=False,
            stage=stage
        )
    
        matching_results["Even-Even Last → First"] = match_sheets(
            current_even_sheets,
            current_even_sheets,
            current_sheets,
            reverse=True,
            odd_even=False,
            same_direction=False,
            stage=stage
        )
    
    # ========================================================
    # STAGE 2 ONWARDS - SAME DIRECTION MATCHING
    # ========================================================   
    if stage >= 2 or final_residual:    
        # ----------------------------------------------------
        # Odd → Odd : Same Direction
        # ----------------------------------------------------
        if len(current_odd_sheets) > 0:    
            matching_results["Same Direction Odd-Odd First → Last"] = match_sheets(
                current_odd_sheets,
                current_odd_sheets,
                current_sheets,
                reverse=False,
                odd_even=False,
                same_direction=True,
                stage=stage)
            
            matching_results["Same Direction Odd-Odd Last → First"] = match_sheets(
                current_odd_sheets,
                current_odd_sheets,
                current_sheets,
                reverse=True,
                odd_even=False,
                same_direction=True,
                stage=stage)   
        # ----------------------------------------------------
        # Odd → Even : Same Direction
        # ----------------------------------------------------
        if (len(current_odd_sheets) > 0
            and len(current_even_sheets) > 0):    
            matching_results["Same Direction Odd-Even First → Last"] = match_sheets(
                current_odd_sheets,
                current_even_sheets,
                current_sheets,
                reverse=False,
                odd_even=True,
                same_direction=True,
                stage=stage)
            
            matching_results["Same Direction Odd-Even Last → First"] = match_sheets(
                current_odd_sheets,
                current_even_sheets,
                current_sheets,
                reverse=True,
                odd_even=True,
                same_direction=True,
                stage=stage)    
        # ----------------------------------------------------
        # Even → Odd : Same Direction
        # ----------------------------------------------------
        if (len(current_even_sheets) > 0
            and len(current_odd_sheets) > 0):   
            matching_results["Same Direction Even-Odd First → Last"] = match_sheets(
                current_even_sheets,
                current_odd_sheets,
                current_sheets,
                reverse=False,
                odd_even=True,
                same_direction=True,
                stage=stage)
    
            matching_results["Same Direction Even-Odd Last → First"] = match_sheets(
                current_even_sheets,
                current_odd_sheets,
                current_sheets,
                reverse=True,
                odd_even=True,
                same_direction=True,
                stage=stage)    
        # ----------------------------------------------------
        # Even → Even : Same Direction
        # ----------------------------------------------------
        if len(current_even_sheets) > 0:    
            matching_results["Same Direction Even-Even First → Last"] = match_sheets(
                current_even_sheets,
                current_even_sheets,
                current_sheets,
                reverse=False,
                odd_even=False,
                same_direction=True,
                stage=stage)
            
            matching_results["Same Direction Even-Even Last → First"] = match_sheets(
                current_even_sheets,
                current_even_sheets,
                current_sheets,
                reverse=True,
                odd_even=False,
                same_direction=True,
                stage=stage)        
            
    # Check whether any matching method produced a valid match
    valid_methods = {method: result
        for method, result in matching_results.items()
        if not result["no_match"]}
    
    if not valid_methods:
    
        if not final_residual:
    
            print("\nNo further normal matching is possible.")
            print("Entering Final Residual Matching...")
    
            final_residual = True
            continue
    
        else:
    
            print("\nFinal Residual Matching failed.")
            break

    # ========================================================
    # COMPARISON
    # ========================================================   
    print("\n============================================================")
    print("             UNMATCHED SHEETS COMPARISON")
    print("============================================================")    
    for method, result in matching_results.items():           
        if stage ==1:    
            print(f"{method:<25} : "
                f"{result['unmatched_percentage']:.2f} % unmatched")    
        else:    
            c_value = result["c"]    
            if c_value is None:
                c_text = f"No Match"
            else:
                c_text = f"{c_value:.2f} mm"    
            print(f"{method:<40} : "
                f"{result['unmatched_percentage']:.2f} % unmatched"
                f" | C = {c_text}")
                        

    #-------------------------------------------
    #       Select Best Matching Method
    #-------------------------------------------
    if stage ==1: #Stage 1: Selection only based on Min Unmatched %
        best_method, best_result = min(matching_results.items(), key=lambda x: x[1]["unmatched_percentage"])
    else: #Stage 2: First Filter methods based on allowable C Value
        allowable_methods = {}
        opposite_c_limit = p * 0.35
        same_c_limit = 20
        for method, result in matching_results.items():
            c_value = result["c"]
            if c_value is None:
                continue
            if "Same Direction" in method: # Same Direcrtion Matching
                if c_value < same_c_limit:
                    allowable_methods[method] = result
            else:
                if c_value <= opposite_c_limit: # Opposite Direction Matching
                    allowable_methods[method] = result
        # ---------------------------------------------------
        # Check Weather Any Methods Satisfies C Condition
        # ---------------------------------------------------
        if not allowable_methods:
        
            if not final_residual:
                print("\nNo matching method satisfies the allowable C condition.")
                print("Entering Final Residual Matching...")
        
                final_residual = True
                continue
        
            else:
                print("\nFinal Residual Matching failed.")
                break
        # -----------------------------------------------------------------------------------
        # Among allowable methods: 1. Minimum unmatched percentage, 2. If tied, minimum C
        # -----------------------------------------------------------------------------------
        best_method, best_result = min(allowable_methods.items(), key=lambda x: (x[1]["unmatched_percentage"],x[1]["c"]))

    # ========================================================
    # BEST MATCHING RESULT FOR THIS STAGE
    # ========================================================
    print("\n============================================================")
    print(f"             BEST MATCHING - STAGE {stage}")
    print("============================================================")
    print("Matching Method     :", best_method)
    print("Reference Sheet     :",best_result["reference_no"])
    print("Best Match Sheet    :",best_result["best_match"])
    print("SHM                 :",f"{best_result["shm"]:.2f} mm")
    print("C                   :",f"{best_result["c"]:.2f} mm")
    print("Matched Sheets      :",best_result["matched"])
    print("Unmatched Sheets    :",best_result["unmatched"])
    print("Unmatched Percentage:",f"{best_result['unmatched_percentage']:.2f} %")

    # Show actual matched sheets
    print("Matched Sheet Nos.  :",[sheet[0] for sheet in best_result["matched_sheets"]])

    # ========================================================
    # GET REMAINING UNMATCHED SHEETS
    # ========================================================
    current_sheets = get_unmatched_sheets(current_sheets,best_result["matched_sheets"])
    print("\nRemaining Sheet Nos.:")
    print([sheet[0] for sheet in current_sheets])

    # Stop when nothing remains
    if len(current_sheets) == 0:
        print("\n============================================================")
        print("       ALL SHEETS SUCCESSFULLY MATCHED")
        print("============================================================")
        break
    
    stage += 1 # Move to nex  stage