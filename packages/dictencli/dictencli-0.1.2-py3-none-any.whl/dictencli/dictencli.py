# imports
import requests
import json
import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich import box
from playsound import playsound

# api's
url_ox = 'https://oxford.vercel.app/word/'
url_mw = 'https://www.dictionaryapi.com/api/v3/references/thesaurus/json/'
key_th = 'adb43bec-8f08-440b-bff7-61f9347ee298'

dict_app = typer.Typer()
console = Console()

# table for meaning
table_mean = Table(show_header=True, header_style="bold #219F94",style="#e30050", box=box.SIMPLE_HEAVY)
table_mean.add_column("Word", style="bold #FFE162", width=15)
table_mean.add_column("Meaning",style="#FFFFFF")

# table for example 
table_exam = Table(show_header=True, header_style="bold #219F94",style="#e30050", box=box.SIMPLE_HEAVY)
table_exam.add_column("Word", style="bold #FFE162", width=12)
table_exam.add_column("Example",style="#FFFFFF")

# table for origin
table_origin = Table(show_header=True, header_style="bold #219F94",style="#e30050", box=box.SIMPLE_HEAVY)
table_origin.add_column("Word", style="bold #FFE162", width=12)
table_origin.add_column("Origin/Etymology",style="#FFFFFF")

# table for antonyms
table_ant = Table(show_header=True, header_style="bold #219F94",style="#e30050", box=box.SIMPLE_HEAVY)
table_ant.add_column("Word", style="bold #FFE162", width=12)
table_ant.add_column("Antonyms",style="#FFFFFF")

# table for synonyms
table_syn = Table(show_header=True, header_style="bold #219F94",style="#e30050", box=box.SIMPLE_HEAVY)
table_syn.add_column("Word", style="bold #FFE162", width=12)
table_syn.add_column("Synonyms",style="#FFFFFF")

# table for phrases
table_phr = Table(show_header=True, header_style="bold #219F94",style="#e30050", box=box.SIMPLE_HEAVY)
table_phr.add_column("Word", style="bold #FFE162", width=12)
table_phr.add_column("Phrases",style="#FFFFFF")

# cli-dicitonary-en, available fucntionalities:
# ['origin','example','synonyms','antonymns','pronunciation','phrases']
@dict_app.command()
def look(word:str,
origin:Optional[bool]=typer.Option(False,'-origin','-or'),
example:Optional[bool]=typer.Option(False,'-example','-ex'),
synonyms:Optional[bool]=typer.Option(False,'-synonyms','-syn'),
antonyms:Optional[bool]=typer.Option(False,'-antonyms','-ant'),
pronunciation:Optional[bool]=typer.Option(False,'-pronunciation','-pro'),
phrases:Optional[bool]=typer.Option(False,'-phrases','-phr')
):  
    """
        use dicten-cli [Options] word[required]
        Options:
            1. orgin: use either '-origin' or '-or'
            2. example: use either '-example' or '-ex'
            3. synonyms: use either 'synonyms' or '-syn'
            4. antonyms: use either '-antonyms' or '-ant'
            5. pronunciation: use either '-pronunciation' or '-pro'
            6. phrases: use either '-phrases' or '-pro'
    """
    
    with console.status("[bold #219F94]hold on...[/bold #219F94]",spinner='dots8Bit',spinner_style="bold #e30050") as status:
        word = word.lower().strip()
        data_ox = requests.get(f"{url_ox+word}")
        data_mw = requests.get(f"{url_mw+word+'?'+'key='+key_th}")
        # data_ox = requests.get(f"{url_ox+language+'/'+word}",headers = {'app_id':api_id,'app_key':api_key})
        word = word.capitalize()

        # origin
        if origin:
            origin_found = False
            try:
                origin = data_ox.json()['results'][0]['lexicalEntries'][0]['entries'][0]['etymologies'][0]
                table_origin.add_row(word,f"[#e30050]➜[/#e30050] Origin: {origin}")
                origin_found = True
            except KeyError:console.print(f"[#e30050]✖[/#e30050] Sorry, no origin for [bold yellow]{word}[/bold yellow] found.")
            finally:
                if origin_found:console.print(table_origin)
                else:return None

        # example
        elif example:
            example_found = False
            try:
                example1 = data_ox.json()['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['examples'][0]['text'].strip()
                table_exam.add_row(word,f"[#e30050]➜[/#e30050] {example1}")
                example_found = True
            except KeyError:
                console.print(f"[#e30050]✖[/#e30050] Sorry, no example related to [bold yellow]{word}[/bold yellow] found.")
            try:
                example2 = data_ox.json()['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][1]['examples'][0]['text'].strip()
                senses = data_ox.json()['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][1]
                if (senses):
                    table_exam.add_row('',f"[#e30050]➜[/#e30050] {example2}")
            except IndexError:return None
            except KeyError:return None
            finally:
                if example_found:console.print(table_exam)
                else:return None

        # synonyms
        elif synonyms:
            synonyms_found = False
            synonyms = data_mw.json()[0]['meta']['syns'][0]
            try:
                if len(synonyms) > 0:
                    synonyms_found = True
                    for idx, synonym in enumerate(synonyms):
                        if idx == 0:
                            table_syn.add_row(word,f"[#e30050]➜[/#e30050] {synonym}")
                        else:
                            table_syn.add_row('',f"[#e30050]➜[/#e30050] {synonym}")             
            except KeyError:console.print(f"[#e30050]✖[/#e30050] Sorry, no synonyms related to [bold yellow]{word}[/bold yellow] found.")
            finally:
                if synonyms_found:
                    console.print(table_syn)
                else:return None

        # antonyms
        elif antonyms:
            antonyms_found = False 
            antonyms = data_mw.json()[0]['meta']['ants'][0]  	
            try:
                if len(antonyms) > 0:
                    antonyms_found = True
                    for idx, antonym in enumerate(antonyms):
                        if idx == 0:
                            table_ant.add_row(word,f"[#e30050]➜[/#e30050] {antonym}")
                        else:
                            table_ant.add_row('',f"[#e30050]➜[/#e30050] {antonym}")
            except Exception:
                console.print(f"[#e30050]✖[/#e30050] Sorry, no antonyms related to [bold yellow]{word}[/bold yellow] found.")
            finally:
                if antonyms_found:
                    console.print(table_ant)
                else:
                    return None

        # pronunciation
        elif pronunciation:
            try:
                pronounce = data_ox.json()['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']
                playsound(pronounce)
            except Exception:
                console.print(f"[#e30050]✖[/#e30050] Sorry, no pronunciation for [bold yellow]{word}[/bold yellow] found.")
        
        # phrases
        elif phrases:
            phrases_found = False
            try:
                phrases = data_ox.json()['results'][0]['lexicalEntries'][0]['phrases']
                if phrases:
                    phrases_found = True
                    i = 0
                    while i < len(phrases):
                        if i == 0:
                            table_phr.add_row(word, f"[#e30050]➜[/#e30050] {phrases[i]['text']}")
                        else:
                            table_phr.add_row('',f"[#e30050]➜[/#e30050] {phrases[i]['text']}")
                        i += 1
            except Exception:
                console.print(f"[#e30050]✖[/#e30050] Sorry, no phrases for [bold yellow]{word}[/bold yellow] found.")
            finally:
                if phrases_found:
                    console.print(table_phr)
                else:
                    return None

        # meaning
        elif not (origin and example and synonyms and antonyms):
            meaning_found = False
            try:
                meanings = data_mw.json()[0]['shortdef']
                if len(meanings) > 0: 
                    meaning_found = True   
                    for idx, meaning in enumerate(meanings):
                        if idx == 0:
                            table_mean.add_row(word,f"[#e30050]➜[/#e30050] {meaning}")
                        else:
                            table_mean.add_row('',f"[#e30050]➜[/#e30050] {meaning}")
            except KeyError:
                console.print(f"[#e30050]✖[/#e30050] Sorry, no such word [bold yellow]{word}[/bold yellow] found.")
            except TypeError:
                 console.print(f"[#e30050]✖[/#e30050] Sorry, no such word [bold yellow]{word}[/bold yellow] found.")
            finally:
                if meaning_found:
                    console.print(table_mean)
                else:
                    return None

@dict_app.command()
def help():
    markdown = """
            Commands:
            1. look - used with optional flags below provided.
                `dictencli look word`
            2. help - will just show you the help options dicussed above
                `dictencli help`
            3. about
                `dictencli about`

            Optional flags:
			1. orgin: use either '-origin' or '-or'
			2. example: use either '-example' or '-ex'
			3. synonyms: use either 'synonyms' or '-syn'
			4. antonyms: use either '-antonyms' or '-ant'
			5. pronunciation: use either '-pronunciation' or '-pro'
			6. phrases: use either '-phrases' or '-phr'

        """
    md = Markdown(markdown)
    console.print(md)

@dict_app.command()
def about():
    console.print("[bold #e30050]Made by Nikhil Omkar as a project for résumé. 🤗[bold /#e30050]")