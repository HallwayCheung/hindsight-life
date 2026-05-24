"use client";

export function PortalBackground() {
  return (
    <div
      className="fixed inset-0 pointer-events-none"
      style={{
        zIndex: 0,
        backgroundColor: "#F9F8F6",
        backgroundImage:
          "radial-gradient(ellipse at 20% 50%, rgba(217, 119, 6, 0.04) 0%, transparent 50%), radial-gradient(ellipse at 80% 20%, rgba(5, 150, 105, 0.04) 0%, transparent 50%)",
      }}
    />
  );
}
