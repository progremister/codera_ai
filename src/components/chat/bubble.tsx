"use client";
import React from "react";
import { Message } from "ai";
import { Grid } from "react-loader-spinner";
import { renderToString } from "react-dom/server";
import { AiOutlineTool, AiOutlineWarning } from "react-icons/ai";
import { Button } from "@/components/ui/button";
import { BsLightningCharge } from "react-icons/bs";
import ReactMarkdown from "react-markdown";
import {
  Download
  } from "lucide-react";

export default function Bubble({
  message,
  loading = false,
  isFirst = false,
  id,
}: {
  message: Message;
  loading?: boolean;
  isFirst?: boolean;
  id: number | string;
}) {
  const rateResponse = async (rate: number) => {
    
    if(rate === -1) {
      document.getElementById('rateUp')?.remove()
    } else if(rate === 1) {
      document.getElementById('rateDown')?.remove()
    } else {
      return;
    }

    const data = {
      api_key: process.env.MENDABLE_API_KEY,
      message_id: id,
      rating_value: rate,
    };
    console.log(`Key: ${data.api_key} Id: ${data.api_key} Rate: ${data.rating_value}`);

    const req = await fetch("https://api.mendable.ai/v0/rateMessage", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .catch((error) => console.error("Error:", error));
  };

  const renderToolContent = (toolName: string, success: boolean) => {
    if (success) {
      return <BsLightningCharge className="ms-mr-1 ms-fill-yellow-400" size={18} />;
    } else {
      return <AiOutlineTool size={20} />;
    }
  };

  return (
    <div
      key={message.id}
      className={`flex gap-3 my-4 text-gray-600 text-sm flex-1 ${
        message.role === "user" ? " justify-end text-right" : ""
      }`}
    >
      {message.role === "user" ? (
        <div className="flex justify-end leading-relaxed bg-white rounded-b-xl rounded-tl-xl text-black p-4">
          <p className="leading-relaxed">
            <span className="block font-bold text-gray-700">You</span>
            {!loading && message.content}
            {loading && (
              <Grid
                height={12}
                width={12}
                radius={5}
                ariaLabel="grid-loading"
                color="#1a1a1a"
                ms-visible={true}
              />
            )}
          </p>
        </div>
      ) : (
        <div className="flex gap-2">
          <img
            src="images/codera_image.png"
            className="h-12 w-12 rounded-full bg-white"
            alt="assistant"
          />
          <div className="leading-relaxed bg-white rounded-b-xl rounded-tr-xl text-black p-4 relative">
            <div className="flex gap-3">
              <span className="block font-bold text-gray-700">Codera</span>
            {!isFirst && (
              <div className="flex gap-2 top-[1rem] left-20 absolute">
                <button
                  id="rateDown"
                  className="hover:scale-105 pointer"
                  onClick={() => rateResponse(-1)}
                >
                  👎
                </button>
                <button
                  className="hover:scale-105 pointer"
                  onClick={() => rateResponse(1)}
                  id="rateUp"
                >
                  👍
                </button>
              </div>
            )}
            </div>
            
            {!loading && (<div className="relative">
              <ReactMarkdown components={{
                // Custom component for rendering tool icons
                tool_called: ({ children }) => {
                  const [toolName, successString] = children.split("$$");
                  const success = successString === "true";
                  return renderToolContent(toolName, success);
                },
              }} className="pb-6">
                {/* Remove unnecessary escapes and potential injection risks */}
                {message.content
                  .replaceAll(`<|tool_error|>`, "")
                  .replaceAll(
                    /\<\|tool_called[\s\S]*\$\$/g,
                    (match) => match
                  )
                  .replaceAll(`<|loading_tools|>`, "")}
              </ReactMarkdown>
              {!isFirst &&
              <Button className="absolute bottom-0 right-0 bg-transparent text-black pointer">
                <Download />
            </Button>}
            </div>
            )}
            {loading && (
              <Grid
                height={12}
                width={12}
                radius={5}
                ariaLabel="grid-loading"
                color="#1a1a1a"
                ms-visible={true}
              />
            )}
          </div>
        </div>
      )}
    </div>
  );
}