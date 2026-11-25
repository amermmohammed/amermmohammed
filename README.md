<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg"><img alt="Amer Malik Mohammed, web developer in Düsseldorf. An animated skyline where each building is one week of contributions." src="assets/hero-light.svg" width="100%"></picture></p>

<p align="center">
<a href="https://runio.dev"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/nav-website-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/nav-website-light.svg"><img alt="Website" src="assets/nav-website-light.svg"></picture></a>
<a href="https://runio.dev/blog"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/nav-blog-en-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/nav-blog-en-light.svg"><img alt="Blog" src="assets/nav-blog-en-light.svg"></picture></a>
<a href="https://runio.dev/de/blog"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/nav-blog-de-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/nav-blog-de-light.svg"><img alt="Blog (DE)" src="assets/nav-blog-de-light.svg"></picture></a>
<a href="https://runio.dev/ar/blog"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/nav-blog-ar-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/nav-blog-ar-light.svg"><img alt="المدونة" src="assets/nav-blog-ar-light.svg"></picture></a>
<a href="https://www.youtube.com/@amer"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/nav-youtube-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/nav-youtube-light.svg"><img alt="YouTube" src="assets/nav-youtube-light.svg"></picture></a>
<a href="https://www.linkedin.com/in/amermmohammed/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/nav-linkedin-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/nav-linkedin-light.svg"><img alt="LinkedIn" src="assets/nav-linkedin-light.svg"></picture></a>
<a href="https://x.com/ameralrawi"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/nav-x-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/nav-x-light.svg"><img alt="X" src="assets/nav-x-light.svg"></picture></a>
</p>

<p align="center">I work from Düsseldorf on online shops for <a href="https://github.com/winkelwagen-de">Winkelwagen</a> in Berlin.<br>Sometimes I record what I learn. No upload schedule, no promises.</p>

<h3 align="center">A few videos</h3>

<!-- videos:start style=cards -->
<table>
<tr>
<td width="33%" valign="top"><a href="https://www.youtube.com/watch?v=ejH1dROc-rA"><img src="https://i.ytimg.com/vi/ejH1dROc-rA/mqdefault.jpg" alt="An external API in a Shopware app: a nightly sync with Symfony" width="100%"></a><br><a href="https://www.youtube.com/watch?v=ejH1dROc-rA">An external API in a Shopware app: a nightly sync with Symfony</a></td>
<td width="33%" valign="top"><a href="https://www.youtube.com/watch?v=CGFFUEQOvw8"><img src="https://i.ytimg.com/vi/CGFFUEQOvw8/mqdefault.jpg" alt="A page in the Shopware admin: app modules and the Meteor Admin SDK" width="100%"></a><br><a href="https://www.youtube.com/watch?v=CGFFUEQOvw8">A page in the Shopware admin: app modules and the Meteor Admin SDK</a></td>
<td width="33%" valign="top"><a href="https://www.youtube.com/watch?v=2D_NS9BxWqM"><img src="https://i.ytimg.com/vi/2D_NS9BxWqM/mqdefault.jpg" alt="A Shopware app server with Symfony: how the shop registers" width="100%"></a><br><a href="https://www.youtube.com/watch?v=2D_NS9BxWqM">A Shopware app server with Symfony: how the shop registers</a></td>
</tr>
</table>
<!-- videos:end -->

<h3 align="center">Can you leave work on time?</h3>

<details data-game="start"><summary><b>Friday, 16:40. Four bugs before you can go home. Click to start.</b></summary><p><b>16:41.</b> A shop's scheduled task has not run since Tuesday. What do you try?</p><details data-choice="wrong"><summary>Clear the cache</summary><p>Still broken. The cache is innocent this time.</p><p><i>Close this and try another.</i></p></details><details data-choice="correct"><summary>Start the workers</summary><p>Fixed. Scheduled tasks need something running to pick them up.</p><p><b>16:47.</b> You changed an app's <code>manifest.xml</code>, but <code>app:refresh</code> ignores it.</p><details data-choice="wrong"><summary>Run it again, harder</summary><p>Still ignored. Confidence is not a flag.</p><p><i>Close this and try another.</i></p></details><details data-choice="wrong"><summary>Delete the app folder</summary><p>Now you have two problems.</p><p><i>Close this and try another.</i></p></details><details data-choice="correct"><summary>Bump the version</summary><p>Fixed. The refresh sees a new version and reads the manifest.</p><p><b>16:52.</b> Shopware runs in Docker and cannot reach your app server on <code>localhost</code>.</p><details data-choice="correct"><summary>Use <code>host.docker.internal</code></summary><p>Fixed. Inside the container, localhost is the container.</p><p><b>16:58.</b> The app's admin page shows an error after exactly five seconds.</p><details data-choice="wrong"><summary>Make the page load faster</summary><p>Still errors. The admin is waiting for a message.</p><p><i>Close this and try another.</i></p></details><details data-choice="wrong"><summary>Hide the error with CSS</summary><p>Tempting. It is still there, and now you know it.</p><p><i>Close this and try another.</i></p></details><details data-choice="correct"><summary>Send <code>sw-app-loaded</code></summary><p>Fixed. The admin now knows your page is ready.</p><p data-game="win"><b>17:00. All fixed.</b> Nobody noticed anything, which is how you know it went well. Go home.</p></details></details><details data-choice="wrong"><summary>Open every port</summary><p>Still broken, and security would like a word.</p><p><i>Close this and try another.</i></p></details><details data-choice="wrong"><summary>Restart Docker</summary><p>It came back up with exactly the same opinion.</p><p><i>Close this and try another.</i></p></details></details></details><details data-choice="wrong"><summary>Raise the PHP memory limit</summary><p>Still broken, but now it is broken with more memory.</p><p><i>Close this and try another.</i></p></details></details>

<br>

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/certificate-dark.svg"><source media="(prefers-color-scheme: light)" srcset="assets/certificate-light.svg"><img alt="A joke certificate claiming this profile was made entirely by hand and that Claude definitely did not help." src="assets/certificate-light.svg" width="100%"></picture></p>

<details><summary>Still suspicious? Run <code>git blame</code></summary><pre>e5f1a02 (Amer   03:12) every pixel of this profile
9c0d7be (Amer   03:13) was placed by hand
41fe88a (Amer   03:14) using nothing but willpower
d3adb33 (Claude 03:14) You're absolutely right!
7aa01c4 (Amer   03:15) ignore that line</pre></details>
