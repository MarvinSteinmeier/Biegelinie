## Dokumentation Frontend

### 1 Konventionen

#### 1.1 Schreibweise
- camelCase für Functionen & Variablen
- PascalCase fpr Klassen
- snake_case für canvas object types (z.B. "full_circle_part")
- caps SNAKE_CASE für globale Konstanten

#### 1.2 Benennung von Variablen & Funktionen

Variablen & Functionen sind so bennant, dass man möglichst die Verhaltensweise aus dem Namen ablesen kann.

### 2 Kommentare

#### 2.1 Funktions-Kommentare

Im gesamten Frontend wurde (bis auf wenige Ausnahmen) jede einzelne Funktion mit einem
beschreibenden Kommentar versehen, welcher klar beschreibt, was die Funktion macht.

Solch ein Funktions-Kommentar beginnt immer mit dem Namen der Funktion, gefolgt von der eigentlichen Beschreibung. 

Die Kommentare haben keine vorgegebene minnimal/maximal Länge, sondern sollten so lange sein, dass die Funktion erklärt ist.

Beispiel:

```js
/** scaleActiveBeamLength scales the length of the active canvas object
 * if the active object is of type "staight_beam" */
export function scaleActiveBeamLength(canvas, factor) {
	const activeObject = canvas.getActiveObject()
	if (!activeObject || activeObject.type != "straight_beam") return
	const length = activeObject.get("width")
	activeObject.set("width", length * factor)
	canvas.requestRenderAll()
}
```

Optimalerweise, ist die Funktionsweise auch schon ganz oder zumidnest teilweise aus dem Namen der Funktion abzulesen. [Siehe 1 Konventionen](#1-Konventionen)

#### 2.1 Inline-Kommentare

An einigen weiteren Stellen wurde auch innerhalb von Funktionen Kommentare eingefügt, wenn bestimmte Code-Abschnitte schwerer zu verstehen sein könnten.

### 3 Struktur

#### 3.1 Lib-Module

Das Frontend unterliegt einer relativ simplen Ordnerstruktur. Jedes applet ("module") hat einen eigenen Unterordner im "module" Ordner. In diesen Ordner kommt der komplette **applet-spezifische** Code.

Jener Code, der **unverändert(!)** in anderen Applets auch verwendet werden kann, wird im lib Ordner platziert.

Man könnte auch sagen, im lib Ordner befindet sich der "allgemeinere" Code.

#### 3.2 Setup Script

Jedes Applet enthält eine setup.js Datei. Dies ist die einzige JavaScript Datei, die auch im HTML Template eingebunden wird.

Im Setup Script werden alle UI Elemente registriert und relevante Funktionen aus anderen Dateien importiert.
Danach werden die Funktionen mit de UI Elementen (meist direkt per Event Listener) verknüpft.

#### 3.3 config.js

Die für das gesamte Projekt relevanten Konstanten sind in der Datei *lib/config.js* gespeichert.

Diese Variablen sind nicht global verfügbar, sondern müssen per Javascript ES6 Modue Syntax importiert werder, damit sie in einer .js Datei verwendet werden können. [Siehe 4.6 Module Syntax](#46-Module-Syntax)

Wie bereits in [1.1 Schreibweise](#11-Schreibweise) beschrieben, sind alle Namen in conifg.js in Großbuchstaben + Snake Case.

Beispiel:

```js
// distance in pixels between elements to snap
export const SNAP_DISTANCE = 15 
```

### 4 Neu verwendete JavaScript Features

Im Projekt wurden im vergleich zur ersten Version einige neue JavaScript Features verwendet. Im folgenden eine Auflistung dieser Features, mit kurzer Erklärung, bzw. Verlinkugnen zu guten Tutorials/Anleitungen für diese Features.

#### 4.1 Truthy/Falsy values
In JavaScript hat jeder Wert einer Variable, im Kontext von If Abfragen einen sog. Truthy bzw. falsy Wert. Das kann für verscheidene Zwekce verwendet werden. In diesem Projekt wurde es hauptsöchlich verwendet, um zu überrüfgen, ob eine Variable überahupt zugeordnet ist:

```js
export function scaleActiveObject(canvas, factor) {
	const activeObject = canvas.getActiveObject()
	if (!activeObject) return // truthy, bzw. falsy Wert von activeObject für Abfrage relevant
	if (activeObject.type == "straight_beam") scaleActiveBeamLength(canvas, factor)
	if (activeObject.type == "circle_beam") scaleActiveCircleBeam(canvas, factor)
	canvas.requestRenderAll()
}
```

Gutes Erklärvideo dazu: https://www.youtube.com/watch?v=Xp60QbXRAPI

#### 4.2 let & const statt var

let & const sind die "modernere" Art & Weise, JavaScriptVariablen zu deklarieren, da var einige unerwartete & komische Verhaltensweisen, in bestimmten Fällen aufweist.

Gutes ErklärVideo dazu: https://www.youtube.com/watch?v=9WIJQDvt4Us

#### 4.3 async await

Async Await ist eine Syntax um asynchrones JavaScript zu schreiben. Um mit dem Projekt zu arebiten, muss das allerdings nicht bis in die Teife verstanden werden, da async await lediglich, bei den Anfragen ans Backend verwendet wird, und deswegen, i.d.R. nicht für neue Features umgeschrieben werden muss.

Zum Beispiel:

```js
export async function calculate(elements) {	
	try {
		const res = await fetch(`${SERVER_BASE_URL}/_ode_beam_backend`, {
			method: "POST",
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(elements),
		})
		const data = await res.json()
		if (!res.ok) {
			const errMessage = data.message
			const err = new Error(errMessage)
			err.statusCode = res.status
			throw err
		}		
		else return data
	} catch (err) {
		throw err
	}	
}
```

Mehr Details zur Funktionsweise von (async) JavaScript in diesem exzellenten Vortrag: 
https://www.youtube.com/watch?v=8aGhZQkoFbQ

#### 4.4 Arrow functions

Arrow functions sind eine Kurzschreibweise für normale Funktionen, und werden im Projekt ausgiebig verwendet.

Gutes Erklärvideo zu Arrow functions:
https://www.youtube.com/watch?v=h33Srr5J9nY

#### 4.5 template strings

Gute Erklärung zu Template Strings
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals

#### 4.6 Module Syntax

Gutes Erklärvideo zur Module Syntax functions:
https://www.youtube.com/watch?v=cRHQNNcYf6s

### 5 Design

#### 5.1 Schriftarten
**Heebo** (https://fonts.google.com/specimen/Heebo)
Open Font License (https://scripts.sil.org/cms/scripts/page.php?item_id=OFL-FAQ_web)
