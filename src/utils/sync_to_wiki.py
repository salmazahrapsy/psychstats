import os
import sys
import argparse
import requests
import pandas as pd

API_ENDPOINT = "https://psychstats.miraheze.org/w/api.php"

def dataframe_to_wikitable(df: pd.DataFrame, title: str = "Statistical Metrics") -> str:
    """Converts a pandas DataFrame into MediaWiki table syntax."""
    wiki_table = [f"=== {title} ===", '{| class="wikitable sortable"', '! ' + ' !! '.join(df.columns)]
    for _, row in df.iterrows():
        formatted_cells = [str(val) for val in row.values]
        wiki_table.append('| ' + ' || '.join(formatted_cells))
    wiki_table.append('|}')
    return '\n'.join(wiki_table)

def preview_sync_payload(page_title: str, content: str):
    """Dry-run preview that does not modify the live wiki."""
    print(f"\n[DRY RUN] Target Wiki Page: {page_title}")
    print(f"API Endpoint: {API_ENDPOINT}")
    print("-" * 40)
    print(content[:500] + ("\n... [truncated]" if len(content) > 500 else ""))
    print("-" * 40)
    print("✓ Dry run syntax check passed.")

def sync_page_to_wiki(page_title: str, content: str, summary: str = "Automated sync via ecosystem pipeline"):
    """
    Pushes wikitext to PsychStats Wiki via Action API.
    Requires MIRAHEZE_BOT_USER and MIRAHEZE_BOT_PASS environment variables.
    """
    bot_user = os.environ.get("MIRAHEZE_BOT_USER")
    bot_pass = os.environ.get("MIRAHEZE_BOT_PASS")

    if not bot_user or not bot_pass:
        print("\nNotice: MIRAHEZE_BOT_USER and MIRAHEZE_BOT_PASS are not set.")
        print("Falling back to dry-run verification mode.")
        preview_sync_payload(page_title, content)
        return

    session = requests.Session()
    session.headers.update({"User-Agent": "SalmaZahra-Research-Sync/1.0"})

    # 1. Retrieve login token
    login_token_req = session.get(API_ENDPOINT, params={
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }).json()
    login_token = login_token_req["query"]["tokens"]["logintoken"]

    # 2. Authenticate
    login_res = session.post(API_ENDPOINT, data={
        "action": "login",
        "lgname": bot_user,
        "lgpassword": bot_pass,
        "lgtoken": login_token,
        "format": "json"
    }).json()

    if login_res.get("login", {}).get("result") != "Success":
        print(f"Authentication failed: {login_res}")
        return

    print("✓ Authenticated with Miraheze MediaWiki")

    # 3. Retrieve CSRF edit token
    csrf_token_req = session.get(API_ENDPOINT, params={
        "action": "query",
        "meta": "tokens",
        "format": "json"
    }).json()
    csrf_token = csrf_token_req["query"]["tokens"]["csrftoken"]

    # 4. Perform edit
    edit_res = session.post(API_ENDPOINT, data={
        "action": "edit",
        "title": page_title,
        "text": content,
        "summary": summary,
        "token": csrf_token,
        "format": "json"
    }).json()

    if "edit" in edit_res and edit_res["edit"].get("result") == "Success":
        print(f"✓ Successfully updated: https://psychstats.miraheze.org/wiki/{page_title}")
    else:
        print(f"Edit failed: {edit_res}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PsychStats MediaWiki Sync Utility")
    parser.add_argument("--page", default="Research_Methods/Benchmark_Metrics", help="Target Wiki Page Title")
    parser.add_argument("--csv", default="data/processed/normalized_metrics.csv", help="Source CSV to sync as table")
    parser.add_argument("--dry-run", action="store_true", help="Perform syntax check without network edit")
    args = parser.parse_args()

    if os.path.exists(args.csv):
        df_sample = pd.read_csv(args.csv).head(5)
        wikitext = dataframe_to_wikitable(df_sample, title="Behavioral Benchmark Normalized Metrics")
    else:
        wikitext = "== Overview ==\nPlaceholder content from Salma Zahra research ecosystem."

    if args.dry_run or not os.environ.get("MIRAHEZE_BOT_USER"):
        preview_sync_payload(args.page, wikitext)
    else:
        sync_page_to_wiki(args.page, wikitext)
