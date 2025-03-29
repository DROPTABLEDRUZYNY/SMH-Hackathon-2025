"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import { getCsrfToken } from "@/services/authService";

const formSchema = z.object({
  description: z
    .string()
    .min(5, {
      message: "Message must be at least 5 characters.",
    })
    .max(1023, {
      message: "Message must be at most 1023 characters.",
    }),
  collected_kg: z
    .number()
    .min(0, {
      message: "Weight must be a positive number.",
    })
    .max(1000, {
      message: "Weight must be less than 1000 kg.",
    }),
  cleaned_all: z.boolean().default(false),
  before_image: z.any().optional(),
  after_image: z.any().optional(),
});

interface PostCreationFormProps {
  trash_place_id: number;
}

export function PostCreationForm({ trash_place_id }: PostCreationFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      description: "",
      collected_kg: 0,
      cleaned_all: false,
      before_image: undefined,
      after_image: undefined,
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    try {
      setIsSubmitting(true);
      const formData = new FormData();
      formData.append('description', values.description);
      formData.append('collected_kg', values.collected_kg.toString());
      formData.append('trash_place_id', trash_place_id.toString());
      formData.append('cleaned_all', values.cleaned_all.toString());
      
      if (values.before_image) {
        formData.append('before_image', values.before_image);
      }
      if (values.after_image) {
        formData.append('after_image', values.after_image);
      }
      let csrfToken = await getCsrfToken();

      for (let pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
      }

      const response = await fetch('http://localhost:8000/api/activities/', {
        method: 'POST',
        body: formData,
        headers: {
            "X-CSRFToken": csrfToken || "",
          },
          credentials: "include",
      });

      if (!response.ok) {
        throw new Error('Failed to submit post');
      }
      
      form.reset();
    } catch (error) {
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-center">Share what you did</h1>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
          <FormField
            control={form.control}
            name="description"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Description</FormLabel>
                <FormControl>
                  <Textarea
                    placeholder="Write your message here"
                    className="h-32 rounded"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="collected_kg"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Weight (kg)</FormLabel>
                <FormControl>
                  <Input
                    type="number"
                    placeholder="Enter weight in kilograms"
                    className="rounded"
                    {...field}
                    onChange={e => field.onChange(parseFloat(e.target.value))}
                  />
                </FormControl>
                <FormDescription>
                  Enter the weight of collected garbage (kg)
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="cleaned_all"
            render={({ field }) => (
              <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                <FormControl>
                  <input
                    type="checkbox"
                    checked={field.value}
                    onChange={field.onChange}
                    className="h-4 w-4 rounded border-gray-300"
                  />
                </FormControl>
                <div className="space-y-1 leading-none">
                  <FormLabel>Is the area cleaned?</FormLabel>
                  <FormDescription>
                    Check this box if you have completely cleaned the area
                  </FormDescription>
                </div>
              </FormItem>
            )}
          />
          <div className="grid grid-cols-2 gap-4">
            <FormField
              control={form.control}
              name="before_image"
              render={({ field: { onChange, value, ...field } }) => (
                <FormItem>
                  <FormLabel>Before Image</FormLabel>
                  <FormControl>
                    <Input
                      type="file"
                      accept="image/*"
                      className="rounded"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        onChange(file);
                      }}
                      {...field}
                    />
                  </FormControl>
                  <FormDescription>
                    Upload a photo of the area before cleaning
                  </FormDescription>
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="after_image"
              render={({ field: { onChange, value, ...field } }) => (
                <FormItem>
                  <FormLabel>After Image</FormLabel>
                  <FormControl>
                    <Input
                      type="file"
                      accept="image/*"
                      className="rounded"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        onChange(file);
                      }}
                      {...field}
                    />
                  </FormControl>
                  <FormDescription>
                    Upload a photo of the area after cleaning
                  </FormDescription>
                </FormItem>
              )}
            />
          </div>
          <Button 
            type="submit" 
            variant="outline" 
            className="rounded"
            disabled={isSubmitting}
          >
            {isSubmitting ? "Submitting..." : "Submit"}
          </Button>
        </form>
      </Form>
    </div>
  );
}
