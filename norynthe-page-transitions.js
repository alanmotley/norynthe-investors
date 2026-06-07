(() => {
  const root = document.documentElement;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const hasInlinePdfTracking = Array.from(document.scripts).some((script) => {
    return !script.src && script.textContent.includes("pdf_download_clicked");
  });

  const cleanEventText = (value) => String(value || "").replace(/\s+/g, " ").trim().slice(0, 96);

  const getMaterialLabel = (link) => {
    const heading = link.querySelector("h3, strong");
    return cleanEventText(heading?.textContent || link.textContent) || "PDF download";
  };

  const getMaterialTrack = (link) => {
    if (link.closest(".fast-path")) return "First 15 minutes";
    if (link.closest(".review-evidence")) return "Featured previews";
    const section = link.closest(".section, .review-dashboard");
    const sectionLabel = section?.querySelector(".section-label")?.textContent;
    const metaTrack = link.querySelector(".card-meta span")?.textContent;
    return cleanEventText(sectionLabel || metaTrack) || "Uncategorized";
  };

  const getDownloadFileName = (link, destination) => {
    const downloadName = link.getAttribute("download");
    if (downloadName) return downloadName;

    try {
      const url = new URL(destination, window.location.href);
      return url.pathname.split("/").filter(Boolean).pop() || destination;
    } catch {
      return destination.split("/").filter(Boolean).pop() || destination;
    }
  };

  const isPdfDestination = (destination) => {
    try {
      return new URL(destination, window.location.href).pathname.toLowerCase().endsWith(".pdf");
    } catch {
      return String(destination || "").toLowerCase().split("?")[0].endsWith(".pdf");
    }
  };

  const trackInvestorPdfDownload = (link) => {
    if (typeof window.gtag !== "function") return;

    const destination = link.getAttribute("href") || "";
    const material = getMaterialLabel(link);
    const track = getMaterialTrack(link);

    window.gtag("event", "pdf_download_clicked", {
      event_category: "Investor Portal",
      site_area: "Investor Portal",
      page_name: document.body?.dataset.analyticsPage || "Norynthe Investor Access",
      transport_type: "beacon",
      link_text: material,
      material,
      source_area: track,
      track,
      destination,
      file_name: getDownloadFileName(link, destination),
      file_extension: "pdf",
    });
  };

  const showPage = () => {
    window.requestAnimationFrame(() => {
      root.classList.remove("nt-transition-exiting");
      root.classList.add("nt-transition-ready");
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", showPage, { once: true });
  } else {
    showPage();
  }

  window.addEventListener("pageshow", showPage);

  if (!hasInlinePdfTracking && !window.__norynthePdfDownloadTracking) {
    window.__norynthePdfDownloadTracking = true;
    root.dataset.pdfTracking = "ready";
    document.addEventListener("click", (event) => {
      const target = event.target instanceof Element ? event.target : event.target?.parentElement;
      const link = target?.closest("a[href]");
      if (!link || !isPdfDestination(link.getAttribute("href") || "")) return;
      trackInvestorPdfDownload(link);
    });
  } else if (hasInlinePdfTracking) {
    root.dataset.pdfTracking = "inline";
  }

  if (reduceMotion) return;

  document.addEventListener("click", (event) => {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
      return;
    }

    const link = event.target.closest("a[href]");
    if (!link || link.hasAttribute("download")) return;

    const href = link.getAttribute("href");
    if (!href || href.startsWith("#") || /^(mailto:|tel:|javascript:)/i.test(href)) return;
    if (link.target && link.target !== "_self") return;

    let url;
    try {
      url = new URL(href, window.location.href);
    } catch {
      return;
    }

    const samePageHash = url.pathname === window.location.pathname && url.search === window.location.search && url.hash;
    if (url.origin !== window.location.origin || samePageHash) return;

    event.preventDefault();
    root.classList.remove("nt-transition-ready");
    root.classList.add("nt-transition-exiting");

    window.setTimeout(() => {
      window.location.href = url.href;
    }, 180);
  });
})();