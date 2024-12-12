<script>import { createEventDispatcher, tick } from "svelte";
import { BlockLabel, IconButtonWrapper, IconButton } from "@gradio/atoms";
import { Clear, Image as ImageIcon, Maximize, Minimize } from "@gradio/icons";
import {
} from "@gradio/utils";
import { get_coordinates_of_clicked_image } from "./utils";
import Webcam from "./Webcam.svelte";
import { Upload } from "@gradio/upload";
import { FileData } from "@gradio/client";
import { SelectSource } from "@gradio/atoms";
import Image from "./Image.svelte";
export let value = null;
export let label = void 0;
export let show_label;
export let sources = ["upload", "clipboard", "webcam"];
export let streaming = false;
export let pending = false;
export let mirror_webcam;
export let selectable = false;
export let root;
export let i18n;
export let max_file_size = null;
export let upload;
export let stream_handler;
export let stream_every;
export let modify_stream;
export let set_time_limit;
export let show_fullscreen_button = true;
let upload_input;
export let uploading = false;
export let active_source = null;
function handle_upload({ detail }) {
  if (!streaming) {
    value = detail;
    dispatch("upload");
  }
}
function handle_clear() {
  value = null;
  dispatch("clear");
  dispatch("change", null);
}
async function handle_save(img_blob, event) {
  if (event === "stream") {
    dispatch("stream", {
      value: { url: img_blob },
      is_value_data: true
    });
    return;
  }
  pending = true;
  const f = await upload_input.load_files([
    new File([img_blob], `image/${streaming ? "jpeg" : "png"}`)
  ]);
  if (event === "change" || event === "upload") {
    value = f?.[0] || null;
    await tick();
    dispatch("change");
  }
  pending = false;
}
$:
  active_streaming = streaming && active_source === "webcam";
$:
  if (uploading && !active_streaming)
    value = null;
const dispatch = createEventDispatcher();
export let dragging = false;
$:
  dispatch("drag", dragging);
function handle_click(evt) {
  let coordinates = get_coordinates_of_clicked_image(evt);
  if (coordinates) {
    dispatch("select", { index: coordinates, value: null });
  }
}
$:
  if (!active_source && sources) {
    active_source = sources[0];
  }
async function handle_select_source(source) {
  switch (source) {
    case "clipboard":
      upload_input.paste_clipboard();
      break;
    default:
      break;
  }
}
let is_full_screen = false;
let image_container;
const toggle_full_screen = async () => {
  if (!is_full_screen) {
    await image_container.requestFullscreen();
  } else {
    await document.exitFullscreen();
    is_full_screen = !is_full_screen;
  }
};
</script>

<BlockLabel {show_label} Icon={ImageIcon} label={label || "Image"} />

<div data-testid="image" class="image-container" bind:this={image_container}>
	<IconButtonWrapper>
		{#if value?.url && !active_streaming}
			{#if !is_full_screen && show_fullscreen_button}
				<IconButton
					Icon={Maximize}
					label={is_full_screen ? "Exit full screen" : "View in full screen"}
					on:click={toggle_full_screen}
				/>
			{/if}
			{#if is_full_screen && show_fullscreen_button}
				<IconButton
					Icon={Minimize}
					label={is_full_screen ? "Exit full screen" : "View in full screen"}
					on:click={toggle_full_screen}
				/>
			{/if}
			<IconButton
				Icon={Clear}
				label="Remove Image"
				on:click={(event) => {
					value = null;
					dispatch("clear");
					event.stopPropagation();
				}}
			/>
		{/if}
	</IconButtonWrapper>
	<div
		class="upload-container"
		class:reduced-height={sources.length > 1}
		style:width={value ? "auto" : "100%"}
	>
		<Upload
			hidden={value !== null || active_source === "webcam"}
			bind:this={upload_input}
			bind:uploading
			bind:dragging
			filetype={active_source === "clipboard" ? "clipboard" : "image/*"}
			on:load={handle_upload}
			on:error
			{root}
			{max_file_size}
			disable_click={!sources.includes("upload") || value !== null}
			{upload}
			{stream_handler}
		>
			{#if value === null}
				<slot />
			{/if}
		</Upload>
		{#if active_source === "webcam" && (streaming || (!streaming && !value))}
			<Webcam
				{root}
				{value}
				on:capture={(e) => handle_save(e.detail, "change")}
				on:stream={(e) => handle_save(e.detail, "stream")}
				on:error
				on:drag
				on:upload={(e) => handle_save(e.detail, "upload")}
				on:close_stream
				{mirror_webcam}
				{stream_every}
				{streaming}
				mode="image"
				include_audio={false}
				{i18n}
				{upload}
				bind:modify_stream
				bind:set_time_limit
			/>
		{:else if value !== null && !streaming}
			<!-- svelte-ignore a11y-click-events-have-key-events-->
			<!-- svelte-ignore a11y-no-static-element-interactions-->
			<div class:selectable class="image-frame" on:click={handle_click}>
				<Image src={value.url} alt={value.alt_text} />
			</div>
		{/if}
	</div>
	{#if sources.length > 1 || sources.includes("clipboard")}
		<SelectSource
			{sources}
			bind:active_source
			{handle_clear}
			handle_select={handle_select_source}
		/>
	{/if}
</div>

<style>
	.image-frame :global(img) {
		width: var(--size-full);
		height: var(--size-full);
		object-fit: scale-down;
	}

	.image-frame {
		object-fit: cover;
		width: 100%;
		height: 100%;
	}

	.upload-container {
		display: flex;
		align-items: center;
		justify-content: center;

		height: 100%;
		flex-shrink: 1;
		max-height: 100%;
	}

	.reduced-height {
		height: calc(100% - var(--size-10));
	}

	.image-container {
		display: flex;
		height: 100%;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		max-height: 100%;
	}

	.selectable {
		cursor: crosshair;
	}
</style>
